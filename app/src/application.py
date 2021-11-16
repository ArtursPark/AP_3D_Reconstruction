from app.src import parse_commands
from app.src import app_commands
from app.src import app_config

import sys

class ReconstructionApp:
	"""
	Singleton : ReconstructionApp class.
	"""

	#	# Public global member variables.
	G_APP_CONFIG = app_config.Config
	G_APP_INPUT_STREAM = None

	# 	# Private global member variables.
	__m_instance = None

	#	# Constructor method.
	def __init__(self, in_argv=None, in_input_stream=None):
		"""Virtually private constructor."""
		if ReconstructionApp.__m_instance != None:
			raise Exception("Warning, class ReconstructionApp is a singleton.")
		else:
			ReconstructionApp.__m_instance = self
			ReconstructionApp.APP_INPUT_STREAM = in_input_stream
			self.argv = sys.argv
			if in_argv:
				self.argv = in_argv
			self.__m_command_parser = parse_commands.ParseCommands(self.argv)
			self.__m_command = self.__m_command_parser.parse_commands(self.argv[1:2])

	#	# Public member methods.
	def parse_commands(self, in_argv=None):
		if in_argv:
			self.argv = in_argv
		self.__m_command = self.__m_command_parser.parse_commands(in_argv[1:2])

	def run(self):
		app_commands.AppCommands(self.argv, self.__m_command)

	def close(self):
		# TODO : Close all app scope services, potential GUIs.
		print("App Closed.")

	# 	# Static member methods.
	@staticmethod
	def instance(in_argv=None, in_input_stream=None):
		"""Static access instance method."""
		ReconstructionApp.G_APP_CONFIG.instance()
		if ReconstructionApp.__m_instance == None:
			ReconstructionApp(in_argv, in_input_stream)
		return ReconstructionApp.__m_instance
