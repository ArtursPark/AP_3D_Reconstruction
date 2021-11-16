from input_stream.src import enum_input_stream
from reconstruction.src import enum_reconstruction
from app.src import application

import os
import argparse


class ArgumentInterface:
	def __init__(
		self,
		in_short_name,
		in_long_name,
		in_name,
		in_type,
		in_default_value,
		in_help,
	):
		self.__m_short_name = in_short_name
		self.__m_long_name = in_long_name
		self.__m_name = in_name
		self.__m_type = in_type
		self.__m_default_value = in_default_value
		self.__m_help = in_help

		self.__m_value = None

	def parse_argument_value(self, in_value):
		self.__m_value = in_value
		return in_value

	# 	# Public setter and getter methods.
	@property
	def short_name(self):
		return self.__m_short_name

	@short_name.setter
	def short_name(self, in_value):
		self.__m_short_name = in_value

	@property
	def long_name(self):
		return self.__m_long_name

	@long_name.setter
	def long_name(self, in_value):
		self.__m_long_name = in_value

	@property
	def name(self):
		return self.__m_name

	@name.setter
	def name(self, in_value):
		self.__m_name = in_value

	@property
	def type(self):
		return self.__m_type

	@type.setter
	def type(self, in_value):
		self.__m_type = in_value

	@property
	def default_value(self):
		return self.__m_default_value

	@default_value.setter
	def default_value(self, in_value):
		self.__m_default_value = in_value

	@property
	def help(self):
		return self.__m_help

	@help.setter
	def help(self, in_value):
		self.__m_help = in_value

	@property
	def value(self):
		return self.__m_value

	@value.setter
	def value(self, in_value):
		self.__m_value = in_value


class ArgumentPath(ArgumentInterface):
	G_CONST_HELP = "Path to file/directory, depending on the input stream. File if video, a directory if collection of images."

	def __init__(self):
		super().__init__("-p", "--path", "path", str, "", ArgumentPath.G_CONST_HELP)


class ArgumentInputStream(ArgumentInterface):
	G_CONST_HELP = 'Input stream enum, choose between "VIDEO", "IMAGES" and "CAMERA". Camera is chosen by default.'

	def __init__(self):
		super().__init__(
			"-s",
			"--stream",
			"stream",
			str,
			enum_input_stream.EnumInputStream.E_CAMERA_STREAM,
			ArgumentInputStream.G_CONST_HELP,
		)

	def parse_argument_value(self, in_value):
		# Check if its a default value.
		if enum_input_stream.EnumInputStream.E_CAMERA_STREAM is in_value:
			self.__m_value = in_value
			return in_value
		
		# TODO : Switch to switch statement once on python 3.10
		self.__m_value = {
			"IMAGE": enum_input_stream.EnumInputStream.E_FRAME_STREAM,
			"VIDEO": enum_input_stream.EnumInputStream.E_VIDEO_STREAM,
			"CAMERA": enum_input_stream.EnumInputStream.E_CAMERA_STREAM,
		}.get(in_value.upper(), enum_input_stream.EnumInputStream.E_CAMERA_STREAM)
		return self.__m_value


class ArgumentCalibrationPath(ArgumentInterface):
	G_CONST_HELP = "Path to calibration data."

	def __init__(self):
		super().__init__(
			"-c",
			"--calibration",
			"calibration",
			str,
			os.path.join(
				application.ReconstructionApp.G_APP_CONFIG.G_APP_PROJECT_PATH,
				"calibration/data/output/output.txt",
			),
			ArgumentCalibrationPath.G_CONST_HELP,
		)


class ArgumentDisplayStream(ArgumentInterface):
	G_CONST_HELP = "Display input stream, ON/OFF."

	def __init__(self):
		super().__init__(
			"-d",
			"--display_stream",
			"display_stream",
			str,
			enum_input_stream.EnumStreamDisplay.E_OFF,
			ArgumentInputStream.G_CONST_HELP,
		)

	def parse_argument_value(self, in_value):
		# Check if its a default value.
		if enum_input_stream.EnumStreamDisplay.E_OFF is in_value:
			self.__m_value = in_value
			return in_value

		# TODO : Switch to switch statement once on python 3.10
		self.__m_value = {
			"OFF": enum_input_stream.EnumStreamDisplay.E_OFF,
			"ON": enum_input_stream.EnumStreamDisplay.E_ON,
		}.get(in_value.upper(), enum_input_stream.EnumStreamDisplay.E_OFF)
		return self.__m_value


class ArgumentDisplayReconstruction(ArgumentInterface):
	G_CONST_HELP = "Display 3D reconstruction plot, ON/OFF."

	def __init__(self):
		super().__init__(
			"-r",
			"--display_reconstruction",
			"display_reconstruction",
			str,
			enum_reconstruction.EnumReconstructionPlotDisplay.E_OFF,
			ArgumentInputStream.G_CONST_HELP,
		)

	def parse_argument_value(self, in_value):
		# Check if its a default value.
		if enum_reconstruction.EnumReconstructionPlotDisplay.E_OFF is in_value:
			self.__m_value = in_value
			return in_value

		# TODO : Switch to switch statement once on python 3.10
		self.__m_value = {
			"OFF": enum_reconstruction.EnumReconstructionPlotDisplay.E_OFF,
			"ON": enum_reconstruction.EnumReconstructionPlotDisplay.E_ON,
		}.get(in_value.upper(), enum_reconstruction.EnumReconstructionPlotDisplay.E_OFF)
		return self.__m_value


class ArgumentList:
	def __init__(self):
		self.__m_list = [
			ArgumentPath(),
			ArgumentInputStream(),
			ArgumentCalibrationPath(),
			ArgumentDisplayStream(),
			ArgumentDisplayReconstruction(),
		]

	@property
	def list(self):
		return self.__m_list

	@list.setter
	def list(self, in_value):
		self.__m_list = in_value

class ArgumentParser:
	def __init__(self, argv):
		self.__m_parser = argparse.ArgumentParser(
			prog=application.ReconstructionApp.G_APP_CONFIG.G_APP_NAME,
			description=application.ReconstructionApp.G_APP_CONFIG.G_APP_DESCRIPTION,
		)
		self.__m_argList: ArgumentList = ArgumentList()
		for argument in self.__m_argList.list:
			self.__m_parser.add_argument(
				argument.short_name,
				argument.long_name,
				default=argument.default_value,
				type=argument.type,
				help=argument.help,
			)

		arguments = self.__m_parser.parse_args(argv)

		self.__m_argument_dictionary = dict()
		for argument in self.__m_argList.list:
			value = argument.parse_argument_value(getattr(arguments, argument.name))
			self.__m_argument_dictionary[argument.name] = value

	@property
	def argument_dictionary(self):
		return self.__m_argument_dictionary

	@argument_dictionary.setter
	def argument_dictionary(self, in_value):
		self.__m_argument_dictionary = in_value