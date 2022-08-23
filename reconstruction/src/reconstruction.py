from typing import Tuple
from features.src.feature_detection import FeatureDetector
from features.src.feature_matching import FeatureMatcher

from pose.src.essential_matrix import EssentialMatrix
from triangulation.src.triangulation import Triangulator
from optimization.src.optimizer_producer_interface import BundleAdjustmentProducer
from optimization.src import bundle_adjustment

from ap_vision.src.data import frame_data as ap_frame_data
from ap_vision.src.data import stream_data as ap_stream_data
from ap_vision.src.visualize import visualize_frame
from ap_vision.src.data.projection_matrix import ProjectionMatrix

import cv2
import numpy
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from scipy.optimize import least_squares


class Reconstruction:
	"""
	Reconstruction class.
	"""

	S_FRAME_WINDOW = visualize_frame.ViewFrame("REGULAR")

	def __init__(
		self,
		in_stream_data: ap_stream_data.StreamData,
		in_is_display_stream: bool = False,
		in_is_display_reconstruction: bool = False,
	):
		self.__m_stream_data: ap_stream_data.StreamData = in_stream_data
		self.__m_frame_count = 0

		self.__m_data: ap_frame_data.FrameDataList = ap_frame_data.FrameDataList()

		self.__m_is_display_stream: bool = in_is_display_stream
		self.__m_is_display_reconstruction: bool = in_is_display_reconstruction

		self.__m_feature_detector: FeatureDetector = FeatureDetector()
		self.__m_feature_matcher: FeatureMatcher = FeatureMatcher()
		self.__m_triangulator: Triangulator = Triangulator()

	def process_frame(self, in_frame):
		proc_frame = in_frame
		return proc_frame

	def read_frame(self):
		f = self.stream_data.stream_handle.read()
		if f is None or numpy.sum(f) == 0:
			return None
		return self.process_frame(f)

	def compute(self):

		self.data = ap_frame_data.FrameDataList()

		# Prepare the starting frame.
		frame_data = ap_frame_data.FrameData()

		frame_data.frame = self.read_frame()
		if frame_data.frame is None:
			return None

		frame_data.stream_id = self.stream_data.stream_id
		frame_data.projection_matrix = ProjectionMatrix()
		frame_data.projection_matrix.compose(
			self.stream_data.calibration_matrix,
			numpy.eye(3),
			numpy.zeros((3, 1)),
		)
		(
			frame_data.feature_points,
			frame_data.descriptors,
		) = self.feature_detector.compute(
			cv2.cvtColor(frame_data.frame, cv2.COLOR_BGR2GRAY)
		)
		self.data.append_frame(frame_data)

		# Start the loop and process each frame while collecting the data.
		while True:

			# Set up this loops previous and current frame data.
			previous_frame_data = self.data.frame_data_list[
				-1
			]  # Get recent frame data.
			current_frame_data = ap_frame_data.FrameData()

			# Read and save frame.
			current_frame_data.frame = self.read_frame()
			if current_frame_data.frame is None:
				break
			current_frame_data.stream_id = self.stream_data.stream_id

			# Compute and save feature points.
			(
				current_frame_data.feature_points,
				current_frame_data.descriptors,
			) = self.feature_detector.compute(
				cv2.cvtColor(current_frame_data.frame, cv2.COLOR_BGR2GRAY)
			)

			# Compute and save feature matching.
			current_frame_data.feature_matches = self.feature_matcher.compute(
				previous_frame_data.descriptors,
				current_frame_data.descriptors,
			)

			# Compute point lists and apply Lowe's ratio test
			prev_points = list()
			current_frame_data.image_points = list()
			current_feature_matches = list()
			feature_count = 0
			for feature_match_m, feature_match_n in current_frame_data.feature_matches:
				if feature_match_m.distance / feature_match_n.distance < 0.75:
					prev_points.append(
						previous_frame_data.feature_points[feature_match_m.queryIdx].pt
					)
					current_frame_data.image_points.append(
						current_frame_data.feature_points[feature_match_m.trainIdx].pt
					)
					current_feature_matches.append((feature_count, feature_count))
					feature_count += 1
			current_frame_data.feature_matches = numpy.array(current_feature_matches)

			prev_points = numpy.array(prev_points)
			current_frame_data.image_points = numpy.array(
				current_frame_data.image_points
			)

			# Compute essential matrix.
			(essential_matrix, mask) = EssentialMatrix.compute(
				prev_points,
				current_frame_data.image_points,
				self.stream_data.calibration_matrix,
			)

			# Remove outliers, using mask.
			# prev_points = prev_points[mask.ravel() == 1]
			# current_frame_data.image_points = current_frame_data.image_points[mask.ravel() == 1]

			# Compute and save, pose / rotation and translation.
			# cv2.recoverPose() already does cheirality check.
			# The cheirality check means that the triangulated
			# 3D points should have positive depth. That is
			# based on the documentation. However, in practice
			# I have been getting a negative Z point values.
			# TODO : Investigate.
			(
				_,
				current_frame_data.rotation_matrix,
				current_frame_data.translation_matrix,
				mask,
			) = cv2.recoverPose(
				essential_matrix, prev_points, current_frame_data.image_points
			)

			# Remove outliers, using mask.
			# prev_points = prev_points[mask.ravel() == 255]
			# current_frame_data.image_points = current_frame_data.image_points[mask.ravel() == 255]

			# Compute undistorted points for triangulation.
			undistorted_previous_points = prev_points
			undistorted_previous_points = cv2.undistortPoints(
				prev_points,
				self.stream_data.calibration_matrix,
				self.stream_data.distortion_coefficients,
			)

			undistorted_current_points = current_frame_data.image_points
			undistorted_current_points = cv2.undistortPoints(
				current_frame_data.image_points,
				self.stream_data.calibration_matrix,
				self.stream_data.distortion_coefficients,
			)

			# Compute and save projection matrices.
			# TODO : Using an identity matrix for projection matrix and computing triangulation, leads to a lower re-projection error. Investigate why that is the case.
			current_frame_data.projection_matrix = ProjectionMatrix()
			current_frame_data.projection_matrix.compose(
				numpy.eye(3, 3),
				current_frame_data.rotation_matrix,
				current_frame_data.translation_matrix,
			)

			# Compute point triangulation.
			current_frame_data.homogeneous_object_points = self.triangulator.compute(
				previous_frame_data.projection_matrix.data,
				current_frame_data.projection_matrix.data,
				undistorted_previous_points,
				undistorted_current_points,
			)
			current_frame_data.euclidean_object_points = (
				current_frame_data.homogeneous_object_points.copy()
			)
			current_frame_data.euclidean_object_points /= (
				current_frame_data.euclidean_object_points[3]
			)
			current_frame_data.euclidean_object_points = (
				current_frame_data.euclidean_object_points[:3, :]
			)

			# TODO : Remove outliers.
			filtered_3d_points = current_frame_data.euclidean_object_points

			# Show triangulation points.
			if self.is_display_reconstruction:
				trace = go.Scatter3d(
					x=filtered_3d_points[0],
					y=filtered_3d_points[1],
					z=filtered_3d_points[2],
					mode="markers",
					marker=dict(
						size=3,
						color=1,
						colorscale="Viridis",
					),
				)
				layout = go.Layout(
					title="3D Scatter plot", scene=dict(aspectmode="auto")
				)
				fig = go.Figure(data=[trace], layout=layout)
				fig.show()

			# View single compute data
			Reconstruction.S_FRAME_WINDOW.view(current_frame_data.frame)

			# TODO : Compute re-projection points. This is mainly required for BA.
			current_frame_data.re_projection_points = (
				bundle_adjustment.re_projection_points(
					current_frame_data, self.stream_data
				)
			)

			if self.__m_frame_count > 0:
				# TODO : Perform local bundle adjustment.
				# Compute local bundle adjustment.
				ba_local_data = BundleAdjustmentProducer().produce_local(
					previous_frame_data, current_frame_data
				)
				re_projection_points = (
					current_frame_data.re_projection_points[:, 0, :]
					- current_frame_data.image_points
				)
				re_projection_error = bundle_adjustment.compute_residual_error(
					current_frame_data.image_points, re_projection_points
				)
				plt.plot(re_projection_error)
				# plt.show()
				plt.clf()

				SBA_J = bundle_adjustment.build_local_bundle_adjustment_jacobian(
					current_frame_data, ba_local_data
				)

				parameters = BundleAdjustmentProducer().produce_paramater_array(
					self.stream_data, previous_frame_data, current_frame_data, SBA_J.point_list
				)

				res = least_squares(
					bundle_adjustment.calc_fun,
					parameters,
					jac_sparsity=SBA_J,
					verbose=2,
					x_scale="jac",
					ftol=1e-4,
					method="trf",
					args=(SBA_J),
				)
				plt.plot(res.fun)
				plt.show()
				plt.clf()

			# Append current frame data.
			self.data.append_frame(current_frame_data)
			self.__m_frame_count += 1

		# TODO : Perform global bundle adjustment.
		# Compute global bundle adjustment.
		ba_data = BundleAdjustmentProducer().produce(self.data)

		return self.data

	# 	# Public setter and getter methods.

	@property
	def _data(self):
		return self.__m_data

	@_data.setter
	def _data(self, in_value):
		self.__m_data = in_value

	@property
	def stream_data(self):
		return self.__m_stream_data

	@stream_data.setter
	def stream_data(self, in_value):
		self.__m_stream_data = in_value

	@property
	def feature_detector(self):
		return self.__m_feature_detector

	@feature_detector.setter
	def feature_detector(self, in_value):
		self.__m_feature_detector = in_value

	@property
	def feature_matcher(self):
		return self.__m_feature_matcher

	@feature_matcher.setter
	def feature_matcher(self, in_value):
		self.__m_feature_matcher = in_value

	@property
	def triangulator(self):
		return self.__m_triangulator

	@triangulator.setter
	def triangulator(self, in_value):
		self.__m_triangulator = in_value

	@property
	def is_display_stream(self):
		return self.__m_is_display_stream

	@is_display_stream.setter
	def is_display_stream(self, in_value):
		self.__m_is_display_stream = in_value

	@property
	def is_display_reconstruction(self):
		return self.__m_is_display_reconstruction

	@is_display_reconstruction.setter
	def is_display_reconstruction(self, in_value):
		self.__m_is_display_reconstruction = in_value
