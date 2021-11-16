import numpy

class FrameData:
	"""
	Struct : FrameData class.
		This will contain all frame data in uncalibrated format.
	"""

	def __init__(
		self,
		in_frame=None,
		in_camera_number=None,
		in_calibration_matrix=None,
		in_distortion_coefficients=None,
		in_feature_points=None,
		in_descriptors=None,
		in_feature_matches=None,
		in_rotation_matrix=None,
		in_translation_matrix=None,
		in_projection_matrix=None,
		in_image_points=None,
		in_homogeneous_points=None,
		in_euclidean_points = None,
		in_re_projection_points=None,
		in_point_observation_matching=None,
	):
		#   # Frame.
		self.__m_frame = in_frame

		#   # Camera data.
		self.__m_camera_number = in_camera_number
		self.__m_calibration_matrix = in_calibration_matrix
		self.__m_distortion_coefficients = in_distortion_coefficients

		# 	# Feature data.
		self.__m_feature_points = in_feature_points
		self.__m_descriptors = in_descriptors
		self.__m_feature_matches = in_feature_matches

		#   # Pose data.
		self.__m_rotation_matrix = in_rotation_matrix
		self.__m_translation_matrix = in_translation_matrix
		self.__m_projection_matrix = in_projection_matrix

		#   # Point data.
		# Image, 2D points.
		self.__m_image_points = in_image_points
		# World object, 4D points.
		self.__m_homogeneous_points = in_homogeneous_points
		# World object, 3D points.
		self.__m_euclidean_points = in_euclidean_points
		# World object re-projected to image, 2D points.
		self.__m_re_projection_points = in_re_projection_points

		self.__m_point_observation_matching = in_point_observation_matching

	#   #   # Setters and getters.
	# Frame.
	@property
	def frame(self):
		return self.__m_frame

	@frame.setter
	def frame(self, in_value):
		self.__m_frame = in_value

	# Camera number.
	@property
	def camera_number(self):
		return self.__m_camera_number

	@camera_number.setter
	def camera_number(self, in_value):
		self.__m_camera_number = in_value

	# Camera calibration/intrinsic matrix.
	@property
	def calibration_matrix(self):
		return self.__m_calibration_matrix

	@calibration_matrix.setter
	def calibration_matrix(self, in_value):
		self.__m_calibration_matrix = in_value

	# Distortion coefficients.
	@property
	def distortion_coefficients(self):
		return self.__m_distortion_coefficients

	@distortion_coefficients.setter
	def distortion_coefficients(self, in_value):
		self.__m_distortion_coefficients = in_value

	# Feature points.
	@property
	def feature_points(self):
		return self.__m_feature_points

	@feature_points.setter
	def feature_points(self, in_value):
		self.__m_feature_points = in_value

	# Descriptors.
	@property
	def descriptors(self):
		return self.__m_descriptors

	@descriptors.setter
	def descriptors(self, in_value):
		self.__m_descriptors = in_value

	# Feature matches.
	@property
	def feature_matches(self):
		return self.__m_feature_matches

	@feature_matches.setter
	def feature_matches(self, in_value):
		self.__m_feature_matches = in_value

	# Rotation matrix.
	@property
	def rotation_matrix(self):
		return self.__m_rotation_matrix

	@rotation_matrix.setter
	def rotation_matrix(self, in_value):
		self.__m_rotation_matrix = in_value

	# Translation matrix.
	@property
	def translation_matrix(self):
		return self.__m_translation_matrix

	@translation_matrix.setter
	def translation_matrix(self, in_value):
		self.__m_translation_matrix = in_value

	# Translation matrix.
	@property
	def projection_matrix(self):
		return self.__m_projection_matrix

	@projection_matrix.setter
	def projection_matrix(self, in_value):
		self.__m_projection_matrix = in_value

	# Image points.
	@property
	def image_points(self):
		return self.__m_image_points

	@image_points.setter
	def image_points(self, in_value):
		self.__m_image_points = in_value

	# Homogenous points.
	@property
	def homogeneous_points(self):
		return self.__m_homogeneous_points

	@homogeneous_points.setter
	def homogeneous_points(self, in_value):
		self.__m_homogeneous_points = in_value

		self.__m_euclidean_points = (in_value / in_value[3])[:3, :]

	# Euclidean points.
	@property
	def euclidean_points(self):
		return self.__m_euclidean_points

	@euclidean_points.setter
	def euclidean_points(self, in_value):
		self.__m_euclidean_points = in_value

	# Re-projection points.
	@property
	def re_projection_points(self):
		return self.__m_re_projection_points

	@re_projection_points.setter
	def re_projection_points(self, in_value):
		self.__m_re_projection_points = in_value


class FrameDataList:
	def __init__(self):
		self.__m_frame_data_list = list()

		self.__m_calibration_matrix = None
		self.__m_distrortion_coefficients = None

		self.__m_all_euclidean_points = None
		self.__m_all_image_points = None

	def append(self, in_frame_data):
		self.__m_frame_data_list.append(in_frame_data)

	def append_euclidean_points(self, in_points):
		if self.__m_all_euclidean_points is None:
			self.__m_all_euclidean_points = in_points
		else:
			self.__m_all_euclidean_points = numpy.hstack([self.__m_all_euclidean_points, in_points])

	def append_image_points(self, in_points):
		if self.__m_all_image_points is None:
			self.__m_all_image_points = in_points
		else:
			self.__m_all_image_points = numpy.hstack([self.__m_all_image_points, in_points])

	# Setters and getters.
	@property
	def frame_data_list(self):
		return self.__m_frame_data_list

	@frame_data_list.setter
	def frame_data_list(self, in_value):
		self.__m_frame_data_list = in_value

	@property
	def intrinsic_matrix(self):
		return self.__m_intrinsic_matrix

	@intrinsic_matrix.setter
	def intrinsic_matrix(self, in_value):
		self.__m_intrinsic_matrix = in_value

	@property
	def distrortion_coefficients(self):
		return self.__m_distrortion_coefficients

	@distrortion_coefficients.setter
	def distrortion_coefficients(self, in_value):
		self.__m_distrortion_coefficients = in_value
