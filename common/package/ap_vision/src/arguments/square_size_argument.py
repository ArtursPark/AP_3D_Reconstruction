from src.arguments.argument_interface import ArgumentInterface


class SquareSizeArgument(ArgumentInterface):
    # 	# Public global member variables.
    G_CONST_HELP = """Square size in meters."""

    # 	# Python member method overides.
    def __init__(self):
        super().__init__(
            "-z",
            "--square_size",
            "square_size",
            float,
            None,
            0.027,
            SquareSizeArgument.G_CONST_HELP,
        )
