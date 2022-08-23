"""
	File name : dlt.py
	File description : 
		Short and quick script that applies DLT.
"""

from calibration.src.direct_linear_transform import DirectLinearTransform
from ap_vision.src.data.projection_matrix import ProjectionMatrix

from ap_vision.src.arguments.argument_list_interface import ArgumentListInterface
from ap_vision.src.arguments.argument_parser import ArgumentParser
from ap_vision.src.arguments.path_argument import PathArgument
from ap_vision.src.arguments.output_argument import OutputArgument

from io import FileIO

import os
import numpy
import typing


def read_dlt_data(in_path: str) -> typing.Tuple[numpy.ndarray, numpy.ndarray]:

    file_handle: FileIO = open(in_path)

    # First, read the image points 2D. Read until white line, then stop and proceed to the next matrix.
    image_points = list()
    line: bytes = file_handle.readline()
    while len(line.strip()) != 0:
        image_points.append(list(map(numpy.double, line.split())))
        line = file_handle.readline()
    image_points = numpy.array(image_points)

    # Second, read the object points 3D.
    object_points = list()
    line = file_handle.readline()
    while len(line.strip()) != 0:
        object_points.append(list(map(numpy.double, line.split())))
        line = file_handle.readline()
    object_points = numpy.array(object_points)

    return image_points, object_points


class DirectLinearTransformArgumentList(ArgumentListInterface):

    # 	# Python member method overides.
    def __init__(self, in_config):
        super().__init__(
            [
                PathArgument(
                    os.path.join(
                        in_config.project_path(),
                        "./calibration/data/direct_linear_transform/sample_dlt_points.txt",
                    )
                ),
                OutputArgument(
                    os.path.join(
                        in_config.project_path(),
                        "./calibration/data/output/direct_linear_transform/sample_dlt_output.txt",
                    )
                ),
            ]
        )


class DirectLinearTransformCommand:

    G_CONST_DLT_USAGE = """
		Example Input File (Path Argument -p) : First is image points in 2D. Second is object points in 3D.
			"
			1 2
			3 4

			5 6 7
			8 9 10
			"
		Example Output File (Output Argument -o) : Calibration, rotation and translation matrices, in that order.
			"
			1 2 3
			4 5 6
			7 8 9

			1 2 3
			4 5 6
			7 8 9

			1
			2
			3
			"
  	"""
    G_CONST_DLT_DESCRIPTION = " Direct Linear Transform (DLT) Command : dlt	"

    # 	# Static member methods.
    def run(in_path: str, in_output: str):

        image_points, object_points = read_dlt_data(in_path)

        projection_matrix_raw, error = DirectLinearTransform().compute(
            image_points, object_points
        )

        print(
            'Status : Mean L2 distnance between computed image points (using computed projection matrix) and given image points is "'
            + str(error)
            + '".'
        )

        projection_matrix = ProjectionMatrix(projection_matrix_raw)

        (
            calibration_matrix,
            rotation_matrix,
            translation_matrix,
        ) = projection_matrix.decompose()

        output_directory = os.path.dirname(in_output)
        if not os.path.exists(output_directory):
            print(
                'Warning : Path to output directory does not exist, creating the path = "'
                + in_output
                + '".'
            )
            os.makedirs(output_directory)

        file_handle: FileIO = open(in_output, "a")
        numpy.savetxt(file_handle, calibration_matrix)
        file_handle.write("\n")
        numpy.savetxt(file_handle, rotation_matrix)
        file_handle.write("\n")
        numpy.savetxt(file_handle, translation_matrix)
        file_handle.close()

    def main(in_config, in_argv):
        print("Status : Start direct linear transform.")

        arg_dict = ArgumentParser(
            in_config,
            DirectLinearTransformArgumentList(in_config),
            in_argv,
            DirectLinearTransformCommand.G_CONST_DLT_DESCRIPTION,
            DirectLinearTransformCommand.G_CONST_DLT_USAGE,
        ).argument_dictionary

        path = None
        if "path" in arg_dict.keys():
            path = arg_dict["path"]

        output = None
        if "output" in arg_dict.keys():
            output = arg_dict["output"]

        DirectLinearTransformCommand.run(path, output)

        print("Status : End direct linear transform.")
