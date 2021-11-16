from src.calibration_app import CalibrationApp
from src.calibration_options import CalibrationOptions

import argparse

def argument_parser(in_argument_values):
	parser = argparse.ArgumentParser(
		prog=CalibrationApp.G_APP_CONFIG.G_CONST_APP_NAME,
		description=CalibrationApp.G_APP_CONFIG.G_CONST_APP_DESCRIPTION,
	)

	parser.add_argument(
		"-p",
		"--path",
		default=CalibrationApp.G_APP_OPTIONS.G_CONST_ARGUMENT_INPUT_IMAGE_DIR_PATH,
		type=str,
		help=CalibrationApp.G_APP_OPTIONS.G_CONST_HELP_INPUT_DIR_PATH,
	)

	parser.add_argument(
		"-i",
		"--image_file_type",
		default=CalibrationApp.G_APP_OPTIONS.G_CONST_ARGUMENT_IMAGE_FILE_TYPE_SUFFIX,
		type=str,
		help=CalibrationApp.G_APP_OPTIONS.G_CONST_HELP_FILE_TYPE_SUFFIX,
	)

	parser.add_argument(
		"-s",
		"--square_size",
		default=CalibrationApp.G_APP_OPTIONS.G_CONST_ARGUMENT_SQUARE_SIZE,
		type=float,
		help=CalibrationApp.G_APP_OPTIONS.G_CONST_HELP_SQUARE_SIZE,
	)

	parser.add_argument(
		"-r",
		"--rows",
		default=CalibrationApp.G_APP_OPTIONS.G_CONST_ARGUMENT_ROWS,
		type=int,
		help=CalibrationApp.G_APP_OPTIONS.G_CONST_HELP_ROWS,
	)

	parser.add_argument(
		"-c",
		"--columns",
		default=CalibrationApp.G_APP_OPTIONS.G_CONST_ARGUMENT_COLUMNS,
		type=int,
		help=CalibrationApp.G_APP_OPTIONS.G_CONST_HELP_COLUMNS,
	)

	parser.add_argument(
		"-o",
		"--output",
		default=CalibrationApp.G_APP_OPTIONS.G_CONST_ARGUMENT_OUTPUT,
		type=str,
		help=CalibrationApp.G_APP_OPTIONS.G_CONST_HELP_OUTPUT,
	)

	arguments = parser.parse_args(in_argument_values)

	CalibrationOptions.G_ARGUMENT_INPUT_IMAGE_DIR_PATH = arguments.path
	CalibrationOptions.G_ARGUMENT_IMAGE_FILE_TYPE_SUFFIX = arguments.image_file_type
	CalibrationOptions.G_ARGUMENT_SQUARE_SIZE = arguments.square_size
	CalibrationOptions.G_ARGUMENT_ROWS = arguments.rows
	CalibrationOptions.G_ARGUMENT_COLUMNS = arguments.columns
	CalibrationOptions.G_ARGUMENT_OUTPUT = arguments.output

	return (
		arguments.path,
		arguments.image_file_type,
		arguments.square_size,
		arguments.rows,
		arguments.columns,
		arguments.output,
	)



