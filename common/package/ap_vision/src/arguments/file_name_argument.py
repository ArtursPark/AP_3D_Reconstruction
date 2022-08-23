from src.arguments.argument_interface import ArgumentInterface


class FileNameArgument(ArgumentInterface):
    # 	# Public global member variables.
    G_CONST_HELP = """File file type suffix."""

    # 	# Python member method overides.
    def __init__(self):
        super().__init__(
            "-n",
            "--name",
            "name",
            str,
            None,
            "sample_image_",
            FileNameArgument.G_CONST_HELP,
        )
