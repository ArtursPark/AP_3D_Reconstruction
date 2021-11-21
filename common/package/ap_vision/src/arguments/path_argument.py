from src.arguments.argument_interface import ArgumentInterface


class PathArgument(ArgumentInterface):
    # 	# Public global member variables.
    G_CONST_HELP = "Path to file/directory, depending on the input stream. File if video, a directory if collection of images."

    # 	# Python member method overides.
    def __init__(self, in_default : str = ""):
        super().__init__(
            "-p", "--path", "path", str, None, in_default, PathArgument.G_CONST_HELP
        )
