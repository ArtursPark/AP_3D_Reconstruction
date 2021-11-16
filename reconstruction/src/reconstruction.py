from input_stream.src.input_stream_interface import InputStreamInterface
from features.src.feature_detection import FeatureDetector
from features.src.feature_matching import FeatureMatcher
from calibration.src import calibration
from pose.src.essential_matrix import EssentialMatrix
from triangulation.src.triangulation import Triangulate
from optimization.src import bundle_adjustment

from ap_vision.src.data import frame_data as ap_frame_data
from ap_vision.src.visualize import visualize_frame

import cv2
import numpy
import plotly.graph_objects as go


class Reconstruction:
	"""
	Reconstruction class.
 	"""

	S_FRAME_WINDOW = visualize_frame.ViewFrame("REGULAR")

	def __init__(
		self,
		in_input_stream: InputStreamInterface,
		in_calibration_data_path: str,
		in_is_display_stream: bool = False,
		in_is_display_reconstruction: bool = False,
	):
		self.__m_data: ap_frame_data.FrameDataList = ap_frame_data.FrameDataList()
		self.__m_input_stream: InputStreamInterface = in_input_stream

		# Camera Calibration.
		(
			self.__m_calibration_matrix,
			self.__m_distortion_coefficients,
		) = calibration.Calibration.load_calibration(in_calibration_data_path)
		if self.__m_calibration_matrix is None:
			print("Error : Calibration matrix is empty from path = \"" + in_calibration_data_path + "\" , existing...")
			exit()
		if self.__m_distortion_coefficients is None:
			print("Error : Distortion coefficients are empty from path = \"" + in_calibration_data_path + "\" , existing...")
			exit()

		self.__m_is_display_stream: bool = in_is_display_stream
		self.__m_is_display_reconstruction: bool = in_is_display_reconstruction

		self.__m_feature_detector: FeatureDetector = FeatureDetector()
		self.__m_feature_matcher: FeatureMatcher = FeatureMatcher()
		self.__m_triangulate: Triangulate = Triangulate()

	def process_frame(self, in_frame):
		proc_frame = in_frame
		return proc_frame

	def read_frame(self):
		f = self.input_stream.read()
		if f is None or numpy.sum(f) == 0:
			return None
		return self.process_frame(f)

	def compute(self):

		self.data = ap_frame_data.FrameDataList()

		# Prepare the starting frame.
		prev_frame = self.read_frame()
		if prev_frame is None:
			return None
		prev_projection_matrix = numpy.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]])

		camera_count = 0

		# Start the loop and process each frame while collecting the data.
		while True:

			# Set up this loops data struct.
			frame_data = ap_frame_data.FrameData()

			# Read and save frame.
			frame_data.frame = self.read_frame()
			if frame_data.frame is None:
				break

			# Save camera info.
			frame_data.camera_number = camera_count
			frame_data.calibration_matrix = self.calibration_matrix
			frame_data.distortion_coefficients = self.distortion_coefficients

			# Compute feature points.
			# TODO : There is not need to get previous points again. Work around this.
			(prev_feature_points, prev_descriptors,) = self.feature_detector.compute(
				cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
			)
			(feature_points, descriptors,) = self.feature_detector.compute(
				cv2.cvtColor(frame_data.frame, cv2.COLOR_BGR2GRAY)
			)

			# Save feature points and descriptors
			frame_data.feature_points = feature_points
			frame_data.descriptors = descriptors

			# Compute feature matching.
			feature_matches = self.feature_matcher.compute(
				prev_descriptors,
				descriptors,
			)

			# Save feature matches.
			frame_data.feature_matches = feature_matches

			# Compute point lists and apply ratio.trainIdx
			prev_points = list()
			points_2d = list()
			for feature_match_m, feature_match_n in feature_matches:
				if feature_match_m.distance / feature_match_n.distance < 0.75:
					prev_points.append(prev_feature_points[feature_match_m.queryIdx].pt)
					points_2d.append(feature_points[feature_match_m.trainIdx].pt)
			prev_points = numpy.array(prev_points)
			points_2d = numpy.array(points_2d)

			# Compute essential matrix.
			(essential_matrix, mask) = EssentialMatrix.compute(
				prev_points,
				points_2d,
				self.calibration_matrix,
			)

			# Remove outliers, using mask.
			prev_points = prev_points[mask.ravel() == 1]
			points_2d = points_2d[mask.ravel() == 1]

			# Compute pose, rotation and translation.
			# cv2.recoverPose() already does cheirality check.
			# The cheirality check means that the triangulated
			# 3D points should have positive depth. That is
			# based on the documentation. However, in practice
			# I have been getting a negative Z point values.
			(
				points,
				rotation_matrix,
				translation_matrix,
				mask,
			) = cv2.recoverPose(essential_matrix, prev_points, points_2d)

			# Save rotation and translation matrices.
			frame_data.rotation_matrix = rotation_matrix
			frame_data.translation_matrix = translation_matrix

			# Remove outliers, using mask.
			prev_points = prev_points[mask.ravel() == 255]
			points_2d = points_2d[mask.ravel() == 255]

			# Compute undistorted points for triangulation.
			undistorted_previous_points = prev_points
			undistorted_previous_points = cv2.undistortPoints(
				prev_points,
				self.calibration_matrix,
				self.distortion_coefficients,
			)

			undistorted_current_points = points_2d
			undistorted_current_points = cv2.undistortPoints(
				points_2d,
				self.calibration_matrix,
				self.distortion_coefficients,
			)

			# Compute projection matrices.
			curr_projection_matrix = cv2.hconcat([rotation_matrix, translation_matrix])

			projection_matrix_1 = prev_projection_matrix
			projection_matrix_1 = numpy.dot(
				self.calibration_matrix, prev_projection_matrix
			)
			projection_matrix_2 = curr_projection_matrix
			projection_matrix_2 = numpy.dot(
				self.calibration_matrix, curr_projection_matrix
			)

			# Save projection matrix.
			frame_data.projection_matrix = curr_projection_matrix

			# Compute point triangulation.
			points_4d = self.triangulate.compute(
				projection_matrix_1,
				projection_matrix_2,
				undistorted_previous_points,
				undistorted_current_points,
			)
			points_3d = points_4d.copy()
			points_3d /= points_3d[3]
			points_3d = points_3d[:3, :]

			# TODO : Remove outliers.
			filtered_3d_points = points_3d

			# Save 4D homogeneous, 3D, and 2D points.
			frame_data.image_points = points_2d
			frame_data.homogeneous_points = points_4d
			frame_data.euclidean_points = points_3d

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
			Reconstruction.S_FRAME_WINDOW.view(frame_data.frame)

			# Compute re-projection points.
			rotation_vector, _ = cv2.Rodrigues(rotation_matrix)
			re_projection_points, _ = cv2.projectPoints(
				points_3d,
				rotation_vector,
				translation_matrix,
				self.calibration_matrix,
				self.distortion_coefficients,
			)

			# Save re-projected points.
			frame_data.re_projection_points = re_projection_points[:, 0, :]

			# Append everything
			self.data.append_euclidean_points(frame_data.euclidean_points)
			self.data.append_image_points(frame_data.image_points.T)

			# TODO : Perform local bundle adjustment.
			# Compute local bundle adjustment.

			# Save frame data.
			self.data.append(frame_data)

			# Prepare info for the next loop.
			prev_frame = frame_data.frame
			prev_descriptors = descriptors
			prev_projection_matrix = curr_projection_matrix

		# TODO : Perform global bundle adjustment.
		# Compute global bundle adjustment.

		return self.data

	# 	# Public setter and getter methods.
	@property
	def _data(self):
		return self.__m_data

	@_data.setter
	def _data(self, in_value):
		self.__m_data = in_value

	@property
	def input_stream(self):
		return self.__m_input_stream

	@input_stream.setter
	def input_stream(self, in_value):
		self.__m_input_stream = in_value

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
	def triangulate(self):
		return self.__m_triangulate

	@triangulate.setter
	def triangulate(self, in_value):
		self.__m_triangulate = in_value

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

	@property
	def calibration_matrix(self):
		return self.__m_calibration_matrix

	@calibration_matrix.setter
	def calibration_matrix(self, in_value):
		self.__m_calibration_matrix = in_value

	@property
	def distortion_coefficients(self):
		return self.__m_distortion_coefficients

	@distortion_coefficients.setter
	def distortion_coefficients(self, in_value):
		self.__m_distortion_coefficients = in_value
