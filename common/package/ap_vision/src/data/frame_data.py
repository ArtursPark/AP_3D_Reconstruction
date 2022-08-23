from src.data.stream_data import StreamData


class FrameData:
    """
    Struct : FrameData class.
                    This will contain all frame data in uncalibrated format.
    """

    def __init__(
        self,
        in_frame=None,
        in_stream_id=None,
        in_feature_points=None,
        in_descriptors=None,
        in_feature_matches=None,
        in_rotation_matrix=None,
        in_translation_matrix=None,
        in_projection_matrix=None,
        in_image_points=None,
        in_homogeneous_object_points=None,
        in_euclidean_object_points=None,
        in_re_projection_points=None,
    ):
        #   # Frame.
        self.__m_frame = in_frame

        #   # Camera data.
        self.__m_stream_id = in_stream_id

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
        self.__m_homogeneous_object_points = in_homogeneous_object_points
        # World object, 3D points.
        self.__m_euclidean_object_points = in_euclidean_object_points
        self.__m_re_projection_points = in_re_projection_points

    # 	# Setters and getters.
    # Frame.
    @property
    def frame(self):
        return self.__m_frame

    @frame.setter
    def frame(self, in_value):
        self.__m_frame = in_value

    # Camera number.
    @property
    def stream_id(self):
        return self.__m_stream_id

    @stream_id.setter
    def stream_id(self, in_value):
        self.__m_stream_id = in_value

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

    # Homogenous object points.
    @property
    def homogeneous_object_points(self):
        return self.__m_homogeneous_object_points

    @homogeneous_object_points.setter
    def homogeneous_object_points(self, in_value):
        self.__m_homogeneous_object_points = in_value

    # Euclidean object points.
    @property
    def euclidean_object_points(self):
        return self.__m_euclidean_object_points

    @euclidean_object_points.setter
    def euclidean_object_points(self, in_value):
        self.__m_euclidean_object_points = in_value

    # Re projected points.
    @property
    def re_projection_points(self):
        return self.__m_re_projection_points

    @re_projection_points.setter
    def re_projection_points(self, in_value):
        self.__m_re_projection_points = in_value


class FrameDataList:
    def __init__(self) -> None:
        self.__m_frame_data_list = list()
        self.__m_stream_data_list = list()

    def append_frame(self, in_frame_data: FrameData):
        self.__m_frame_data_list.append(in_frame_data)

    def append_stream(self, in_stream_data: StreamData):
        self.__m_stream_data_list.append(in_stream_data)

    # 	# Setters and getters.
    @property
    def frame_data_list(self) -> list:
        return self.__m_frame_data_list

    @frame_data_list.setter
    def frame_data_list(self, in_value: list):
        self.__m_frame_data_list = in_value

    @property
    def stream_data_list(self) -> list:
        return self.__m_stream_data_list

    @stream_data_list.setter
    def stream_data_list(self, in_value: list):
        self.__m_stream_data_list = in_value
