from input_stream.src import input_stream_interface

import cv2


class CameraStream(input_stream_interface.InputStreamInterface):
    
	# 	# Python member method overides.
    def __init__(self):
        super().__init__()
        self.stream_handle = cv2.VideoCapture(0)
        if not self.stream_handle.isOpened():
            print("Error : Cannot open camera.")
            exit()

    # 	# Public virtual member method overides.
    def read(self):
        # TODO : Handle the return value.
        return_value, frame = self.stream_handle.read()
        return frame

    def close(self):
        self.stream_handle.release()
