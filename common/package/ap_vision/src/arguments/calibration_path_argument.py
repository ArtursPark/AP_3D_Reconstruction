from src.arguments.argument_interface import ArgumentInterface

import os


class CalibrationPathArgument(ArgumentInterface):

    # 	# Public global member variables.
    G_CONST_HELP = "Path to calibration data."

    # 	# Python member method overides.
    def __init__(self, in_project_path):
        super().__init__(
            "-a",
            "--calibration",
            "calibration",
            str,
            None,
            os.path.join(
                in_project_path,
                "calibration/data/output/output.txt",
            ),
            CalibrationPathArgument.G_CONST_HELP,
        )
