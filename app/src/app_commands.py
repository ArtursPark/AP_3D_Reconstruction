import calibration.src.calibration_command
import utility_apps.src.video_to_images
import reconstruction.src.reconstruction_command

class AppCommands:
	"""
	AppCommands class.
		This will contain the main commands for the various commands/apps/utilities.
	"""

	# 	# Python member method overides.
	def __init__(self, in_argv, in_command):
		self.__m_argv = in_argv
		getattr(self, in_command)()

	#	# Public member methods.
	def video_to_images(self):
		utility_apps.src.video_to_images.main(self.__m_argv[2:])

	def calibrate(self):
		calibration.src.calibration_command.main(self.__m_argv[2:])

	def reconstruction(self):
		reconstruction.src.reconstruction_command.ReconstructionCommand.main(self.__m_argv[2:])

