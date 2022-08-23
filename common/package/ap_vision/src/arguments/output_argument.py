from src.arguments.argument_interface import ArgumentInterface

import os


class OutputArgument(ArgumentInterface):
    # 	# Public global member variables.
    G_CONST_HELP = "Output to file/directory."

    # 	# Python member method overides.
    def __init__(self, in_default_value="./data/output/"):
        super().__init__(
            "-o",
            "--output",
            "output",
            str,
            None,
            in_default_value,
            OutputArgument.G_CONST_HELP,
        )
