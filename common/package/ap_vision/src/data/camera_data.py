
# TODO : Replace all the duplicated calibration matrix data and distortion coefficients in frame data, with a mapping to camera data in the frame data list.

class CameraData:
    def __init__(self):
        self.__m_id = None
        self.__m_calibration_matrix = None
        self.__m_distortion_coefficients = None