from src.arguments.argument_interface import ArgumentInterface

import argparse


class DisplayStreamArgument(ArgumentInterface):

    # 	# Public global member variables.
    G_CONST_HELP = "Add the argument to display input stream. This is false by default."

    # 	# Python member method overides.
    def __init__(self):
        super().__init__(
            "-d",
            "--display_stream",
            "display_stream",
            bool,
            argparse.BooleanOptionalAction,
            False,
            DisplayStreamArgument.G_CONST_HELP,
        )
