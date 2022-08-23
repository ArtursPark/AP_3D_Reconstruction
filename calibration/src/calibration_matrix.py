class CalibrationMatrix:
    """
    CalibrationMatrix class.
    """

    # 	# Constructor method.
    def __init__(self, in_calibration_matrix=None):
        self.__m_calibration_matrix = in_calibration_matrix

    #   # Setters and getters.
    @property
    def calibration_matrix(self):
        return self.__m_calibration_matrix

    @calibration_matrix.setter
    def calibration_matrix(self, in_value):
        self.__m_calibration_matrix = in_value
