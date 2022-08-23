from src.arguments.argument_interface import ArgumentInterface


class RowsArgument(ArgumentInterface):
    # 	# Public global member variables.
    G_CONST_HELP = """Number of rows."""

    # 	# Python member method overides.
    def __init__(self):
        super().__init__(
            "-r",
            "--rows",
            "rows",
            int,
            None,
            9,
            RowsArgument.G_CONST_HELP,
        )
