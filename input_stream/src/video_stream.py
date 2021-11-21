from input_stream.src import input_stream_interface

import cv2


class VideoStream(input_stream_interface.InputStreamInterface):

    # 	# Python member method overides.
    def __init__(self, in_filepath):
        super().__init__()
        self.__m_stream_handle = cv2.VideoCapture(in_filepath)
        if not self.__m_stream_handle.isOpened():
            print("Error : Cannot open video. Path = " + str(in_filepath))
            exit()

    # 	# Public virtual member method overides.
    def read(self):
        # TODO : handle the return value.
        return_value, frame = self.__m_stream_handle.read()
        return frame

    def close(self):
        self.__m_stream_handle.release()
