import os
from input_stream.src import input_stream_interface

import cv2
import os


class FrameStream(input_stream_interface.InputStreamInterface):
    """
    FrameStream class.
            The object will iterate through all the files in the input directory path, trying to read them all as an image.
    """

    # 	# Python member method overides.
    def __init__(self, in_dirpath):
        super().__init__()
        self.__m_dirpath = in_dirpath
        self.__m_frame_list = os.listdir(in_dirpath)
        self.__m_count = 1
        self.__m_total_frames = len(self.__m_frame_list)

    # 	# Public virtual member method overides.
    def read(self):
        if self.count >= self.total_frames:
            return None
        frame = cv2.imread(os.path.join(self.dirpath, self.__m_frame_list[self.count]))
        self.count = self.count + 1
        return frame

    def close(self):
        return

    # 	# Public setter and getter methods.
    @property
    def frame_list(self):
        return self.__m_frame_list

    @frame_list.setter
    def frame_list(self, in_value):
        self.__m_frame_list = in_value

    @property
    def dirpath(self):
        return self.__m_dirpath

    @dirpath.setter
    def dirpath(self, in_value):
        self.__m_dirpath = in_value

    @property
    def count(self):
        return self.__m_count

    @count.setter
    def count(self, in_value):
        self.__m_count = in_value

    @property
    def total_frames(self):
        return self.__m_total_frames

    @total_frames.setter
    def total_frames(self, in_value):
        self.__m_total_frames = in_value
