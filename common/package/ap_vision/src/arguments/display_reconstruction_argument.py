from src.arguments.argument_interface import ArgumentInterface

import argparse


class DisplayReconstructionArgument(ArgumentInterface):

    # 	# Public global member variables.
    G_CONST_HELP = (
        "Add the argument to display 3D reconstruction plot. This is false by default."
    )

    # 	# Python member method overides.
    def __init__(self):
        super().__init__(
            "-k",
            "--display_reconstruction",
            "display_reconstruction",
            bool,
            argparse.BooleanOptionalAction,
            False,
            DisplayReconstructionArgument.G_CONST_HELP,
        )
