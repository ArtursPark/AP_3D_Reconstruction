from src.arguments.argument_interface import ArgumentInterface


class FileTypeArgument(ArgumentInterface):
    # 	# Public global member variables.
    G_CONST_HELP = """File type extension/suffix."""

    # 	# Python member method overides.
    def __init__(self):
        super().__init__(
            "-t",
            "--type",
            "type",
            str,
            None,
            "jpg",
            FileTypeArgument.G_CONST_HELP,
        )
