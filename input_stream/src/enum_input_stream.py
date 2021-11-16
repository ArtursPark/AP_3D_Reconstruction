import enum
 
class EnumStreamDisplay(enum.Enum):
    E_OFF = 0
    E_ON = 1

class EnumInputStream(enum.Enum):
    E_WRONG_STREAM = 0
    E_FRAME_STREAM = 1
    E_VIDEO_STREAM = 2
    E_CAMERA_STREAM = 3