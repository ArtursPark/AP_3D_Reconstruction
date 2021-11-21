from src.calibration import Calibration
from calibration.src.calibration_argument_list import CalibrationArgumentList

from ap_vision.src.arguments.argument_parser import ArgumentParser

class CalibrationCommand:
    
    # 	# Public global member variables.
	G_CONST_COMMAND_NAME = "Calibration"
	G_CONST_COMMAND_DESCRIPTION = """
		This application is used to do camera calibration, to find intrinsic matrix, and distortion coefficients. 
	"""

    # 	# Public member methods.
	def main(in_config, in_argv):
		print("Status : Start calibration.")

		arg_dict = ArgumentParser(
			in_config, CalibrationArgumentList(in_config), in_argv
		).argument_dictionary

		path = None
		if "path" in arg_dict.keys():
			path = arg_dict["path"]

		type = None
		if "type" in arg_dict.keys():
			type = arg_dict["type"]
		
		square_size = None
		if "square_size" in arg_dict.keys():
			square_size = arg_dict["square_size"]
		
		columns = None
		if "columns" in arg_dict.keys():
			columns = arg_dict["columns"]
		
		rows = None
		if "rows" in arg_dict.keys():
			rows = arg_dict["rows"]
		
		display_stream = None
		if "display_stream" in arg_dict.keys():
			display_stream = arg_dict["display_stream"]
		
		output = None
		if "output" in arg_dict.keys():
			output = arg_dict["output"]

		calibration = Calibration(
			path, square_size, rows, columns, type, output, display_stream
		)
		calibration.compute()

		print("Status : End calibration.")
