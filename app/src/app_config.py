import os


class Config:
	"""
	Singleton : Config class.
		This class will contain values, that are mainly static, and app wide with lifetime of the app.
	"""

	# 	# Public global member variables.
	G_APP_NAME = "AP 3D Reconstruction"
	G_APP_DESCRIPTION = """
		This application is a way to learn photogrammetry concepts and put them into practice. The application will provide a user with an 
		easy way to perform a number of functions, ranging from data acquisition to 3D reconstruction. 
	"""
	G_APP_USAGE = """
	AP 3D Reconstruction <command> [<args>]

		<command>				<description>
		video_to_images			Converts a video into a set of frames.
		calibrate				Calibrates a camera using Zhang's method, creating a file containing an intrinsic matrix, plus distrortion 
								coefficients.
		reconstruction			Reconstructs a set of images into a set of 3D points.               
	"""
	G_APP_AUTHOR_URL = "https://arturspark.com/HTML/index.html"
	G_APP_AUTHOR_EMAIL = "arturspark1995@gmail.com"
	G_APP_GIT_URL = "https://github.com/ArtursPark"
	G_APP_GIT_PROJECT_URL = "https://github.com/ArtursPark/AP_3D_Reconstruction"
	G_APP_PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

	# 	# Private global member variables.
	__m_instance = None

	# 	# Python member method overides.
	def __init__(self):
		"""Virtually private constructor."""
		if Config.__m_instance != None:
			raise Exception("Warning, class Config is a singleton.")
		else:
			Config.__m_instance = self

	# 	# Static member methods.
	@staticmethod
	def instance():
		"""Static access instance method."""
		if Config.__m_instance == None:
			Config()
		return Config.__m_instance
