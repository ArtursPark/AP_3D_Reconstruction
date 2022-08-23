import numpy


# TODO : Add input stream as a type to the stream handle.


class StreamData:
    def __init__(
        self,
        in_stream_id: int,
        in_stream_handle,
        in_calibration_matrix=numpy.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
        in_distortion_coefficients=numpy.array([1, 1, 1, 1, 1]),
    ) -> None:
        self.__m_stream_id: int = in_stream_id
        self.__m_stream_handle = in_stream_handle
        self.__m_calibration_matrix = in_calibration_matrix
        self.__m_distortion_coefficients = in_distortion_coefficients

    # 	# Setters and getters.

    # Stream Id.
    @property
    def stream_id(self) -> int:
        return self.__m_stream_id

    @stream_id.setter
    def stream_id(self, in_value: int):
        self.__m_stream_id = in_value

    # Stream Handle.
    @property
    def stream_handle(self):
        return self.__m_stream_handle

    @stream_handle.setter
    def stream_handle(self, in_value):
        self.__m_stream_handle = in_value

    # Calibration Matrix.
    @property
    def calibration_matrix(self) -> numpy.ndarray:
        return self.__m_calibration_matrix

    @calibration_matrix.setter
    def calibration_matrix(self, in_value: numpy.ndarray):
        self.__m_calibration_matrix = in_value

    # Distortion Coefficients.
    @property
    def distortion_coefficients(self) -> numpy.ndarray:
        return self.__m_distortion_coefficients

    @distortion_coefficients.setter
    def distortion_coefficients(self, in_value: numpy.ndarray):
        self.__m_distortion_coefficients = in_value
