from src.calibration_config import CalibrationConfig

import os

class CalibrationOptions:
    """
	CalibrationOptions class.
	"""

	#	# Public global member variables.
    # Input image directory path argument.
    G_ARGUMENT_INPUT_IMAGE_DIR_PATH : str = ""
    G_CONST_ARGUMENT_INPUT_IMAGE_DIR_PATH : str = os.path.join(CalibrationConfig.G_CONST_APP_ROOT_PATH, "./data/input/")
    G_CONST_HELP_INPUT_DIR_PATH = """Input image directory path."""

    # Image file type suffix argument.
    G_ARGUMENT_IMAGE_FILE_TYPE_SUFFIX : str = ""
    G_CONST_ARGUMENT_IMAGE_FILE_TYPE_SUFFIX = "jpg"
    G_CONST_HELP_FILE_TYPE_SUFFIX = """Image file type suffix."""

    # Square size in meters.
    G_ARGUMENT_SQUARE_SIZE : float = 0.0
    G_CONST_ARGUMENT_SQUARE_SIZE : float = 0.027
    G_CONST_HELP_SQUARE_SIZE = """Square size in meters."""

    # Display the calibration window.
    G_ARGUMENT_DISPLAY : bool = False
    G_CONST_ARGUMENT_DISPLAY : bool = False
    G_CONST_HELP_DISPLAY = """Display the calibration window."""

    # Number of rows.
    G_ARGUMENT_ROWS : int = 0
    G_CONST_ARGUMENT_ROWS : int = 9
    G_CONST_HELP_ROWS = """Number of rows."""

    # Number of columns.
    G_ARGUMENT_COLUMNS : int = 0
    G_CONST_ARGUMENT_COLUMNS : int = 7
    G_CONST_HELP_COLUMNS = """Number of columns."""

    # Output path.
    G_ARGUMENT_OUTPUT : str = ""
    G_CONST_ARGUMENT_OUTPUT : str = os.path.join(CalibrationConfig.G_CONST_APP_ROOT_PATH, "./data/output/output.txt")
    G_CONST_HELP_OUTPUT = """Output path."""
