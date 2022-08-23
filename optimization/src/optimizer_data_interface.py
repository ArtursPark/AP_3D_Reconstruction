import numpy

class SBAPointList:
    def __init__(self) -> None:
        self.sba_list = list()

    def append(
        self,
        in_observation,
        in_frame_index,
        in_point_number,
        in_point,
    ) -> None:
        self.sba_list.append(
            tuple(in_observation, in_frame_index, in_point_number, in_point)
        )


class BundleAdjustmentDataInterface:
    def __init__(self) -> None:
        super().__init__()

        self.__m_camera_id_list = list()
        self.__m_frame_index_list = list()
        self.__m_observation_list = list()
        self.__m_point_index_list = list()
        self.__m_point_list = list()
        self.__m_image_points = list()
        self.parameters = None

    def append(
        self,
        in_camera_id_list,
        in_frame_index,
        in_observation,
        in_point_index,
        in_point,
        in_image_point,
    ):
        self.__m_camera_id_list.append(in_camera_id_list)
        self.__m_frame_index_list.append(in_frame_index)
        self.__m_observation_list.append(in_observation)
        self.__m_point_index_list.append(in_point_index)
        self.__m_point_list.append(in_point)
        self.__m_image_points.append(in_image_point)

    # 	# Setters and getters.

    # Camera Id List.
    @property
    def camera_id_list(self) -> list:
        return self.__m_camera_id_list

    @camera_id_list.setter
    def camera_id_list(self, in_value: list):
        self.__m_camera_id_list = in_value

    # Frame Index List.
    @property
    def frame_index_list(self) -> list:
        return self.__m_frame_index_list

    @frame_index_list.setter
    def frame_index_list(self, in_value: list):
        self.__m_frame_index_list = in_value

    # Observation List.
    @property
    def observation_list(self) -> list:
        return self.__m_observation_list

    @observation_list.setter
    def observation_list(self, in_value: list):
        self.__m_observation_list = in_value

    # Point Index List.
    @property
    def point_index_list(self) -> list:
        return numpy.array(self.__m_point_index_list)

    @point_index_list.setter
    def point_index_list(self, in_value: list):
        self.__m_point_index_list = in_value

    # Point List.
    @property
    def point_list(self) -> list:
        return numpy.array(self.__m_point_list)

    @point_list.setter
    def point_list(self, in_value: list):
        self.__m_point_list = in_value

    # Image Point List.
    @property
    def image_points(self) -> list:
        return numpy.array(self.__m_image_points)

    @image_points.setter
    def image_points(self, in_value: list):
        self.__m_image_points = in_value

    # Frame Data.
    @property
    def frame_data(self) -> list:
        return self.__m_frame_data

    @frame_data.setter
    def frame_data(self, in_value: list):
        self.__m_frame_data = in_value

    # Stream Data.
    @property
    def stream_data(self) -> list:
        return self.__m_stream_data

    @stream_data.setter
    def stream_data(self, in_value: list):
        self.__m_stream_data = in_value


class BundleAdjustmentData(BundleAdjustmentDataInterface):
    def __init__(self) -> None:
        super().__init__()
