from ap_vision.src.arguments.argument_interface import ArgumentInterface

from enum import Enum

class EnumInputStream(Enum):
    E_WRONG_STREAM = 0
    E_FRAME_STREAM = 1
    E_VIDEO_STREAM = 2
    E_CAMERA_STREAM = 3

class InputStreamArgument(ArgumentInterface):
    # 	# Public global member variables.
    G_CONST_HELP = 'Input stream enum, choose between "VIDEO", "IMAGES" and "CAMERA". Camera is chosen by default.'

    # 	# Python member method overides.
    def __init__(self):
        super().__init__(
            "-s",
            "--stream",
            "stream",
            str,
            None,
            EnumInputStream.E_CAMERA_STREAM,
            InputStreamArgument.G_CONST_HELP,
        )

    # 	# Public member methods.
    def parse_argument_value(self, in_value):
        # Check if its a default value.
        if EnumInputStream.E_CAMERA_STREAM is in_value:
            self.__m_value = in_value
            return in_value

        # TODO : Switch to switch statement once on python 3.10
        self.__m_value = {
            "IMAGE": EnumInputStream.E_FRAME_STREAM,
            "VIDEO": EnumInputStream.E_VIDEO_STREAM,
            "CAMERA": EnumInputStream.E_CAMERA_STREAM,
        }.get(in_value.upper(), EnumInputStream.E_CAMERA_STREAM)
        return self.__m_value
