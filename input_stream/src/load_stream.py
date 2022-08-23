from input_stream.src import input_stream_interface

from ap_vision.src.data.stream_data import StreamData

import cv2
import numpy
import os


class LoadStream:
    @staticmethod
    def load(
        in_id: int, in_stream: input_stream_interface.InputStreamInterface, in_path: str
    ) -> StreamData:
        """Loads the stream information.

        Args:
                                        in_id (int): Unique stream identification.
                                        in_stream (input_stream_interface.InputStreamInterface): Child class that inherits from the InputStreamInterface.
                                        in_path (str): Path to stream calibration file.

        Returns:
                                        StreamData: Object containing stream information and a handle.
        """

        default_calibration_matrix = numpy.array(
            [[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=numpy.float64
        )
        default_distortion_coefficients = numpy.array(
            [1, 1, 1, 1, 1], dtype=numpy.float64
        )

        if not os.path.exists(in_path):
            print(
                'Warning : Calibration file does not exist, "'
                + in_path
                + '".'
                + "Setting calibration matrix (3x3 identity) and distrortion coefficients (ones) to default values."
            )
            return StreamData(
                in_id,
                in_stream,
                default_calibration_matrix,
                default_distortion_coefficients,
            )

        # Get camera calibration info.
        file_handle = cv2.FileStorage(
            in_path,
            cv2.FILE_STORAGE_READ,
        )

        calibration_matrix = numpy.asarray(
            file_handle.getNode("calibration_matrix").mat()
        )
        distortion_coefficients = numpy.asarray(
            file_handle.getNode("distortion_coefficients").mat()
        )

        file_handle.release()

        if calibration_matrix is None:
            print(
                'Warning : Calibration matrix is empty from path = "'
                + in_path
                + '" , defaulting to 3x3 identity matrix...'
            )
            calibration_matrix = default_calibration_matrix

        if distortion_coefficients is None:
            print(
                'Warning : Distortion coefficients are empty from path = "'
                + in_path
                + '" , defaulting to an array of ones...'
            )
            distortion_coefficients = default_distortion_coefficients

        return StreamData(in_id, in_stream, calibration_matrix, distortion_coefficients)
