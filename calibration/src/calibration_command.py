from src import calibration_arguments 
from src.calibration import Calibration

def main(argv):
	argument_values = argv
	(
		dir_path,
		image_file_type_suffix,
		square_size,
		rows,
		columns,
		output_path,
	) = calibration_arguments.argument_parser(argument_values)

	calibration = Calibration(
		dir_path, square_size, rows, columns, image_file_type_suffix, output_path
	)
	calibration.run_calibration()
