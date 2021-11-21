from src.arguments.argument_interface import ArgumentInterface


class ColumnsArgument(ArgumentInterface):
    
    # 	# Public global member variables.
    G_CONST_HELP = """Number of columns."""
    
    # 	# Python member method overides.
    def __init__(self):
        super().__init__(
            "-c",
            "--columns",
            "columns",
            int,
            None,
            7,
            ColumnsArgument.G_CONST_HELP,
        )
