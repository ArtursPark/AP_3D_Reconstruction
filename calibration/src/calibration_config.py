import os

class CalibrationConfig:
	"""
	CalibrationConfig class.
	"""

	#	# Public global member variables.
	G_CONST_APP_NAME = "Calibration"
	G_CONST_APP_DESCRIPTION = """
		This application is used to do camera calibration, to find intrinsic matrix, and distortion coefficients. 
	"""
	# Path to calibration dir path.
	G_CONST_APP_ROOT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__))) 