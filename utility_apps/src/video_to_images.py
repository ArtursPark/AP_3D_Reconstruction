"""
	File name : video_to_images.py
	File description : 
		This is a short and quick utility app that will split the video into a set of images and save them in output directory.
"""

from input_stream.src import video_stream

from ap_vision.src.arguments.argument_list_interface import ArgumentListInterface
from ap_vision.src.arguments.argument_parser import ArgumentParser

from ap_vision.src.arguments.path_argument import PathArgument
from ap_vision.src.arguments.file_name_argument import FileNameArgument
from ap_vision.src.arguments.file_type_argument import FileTypeArgument
from ap_vision.src.arguments.output_argument import OutputArgument

import cv2

import os


class VideoToImagesArgumentList(ArgumentListInterface):

    # 	# Python member method overides.
    def __init__(self, in_config):
        super().__init__(
            [
                PathArgument(
                    os.path.join(
                        in_config.project_path(), "./data/input/sample_video.mp4"
                    )
                ),
                FileNameArgument(),
                FileTypeArgument(),
                OutputArgument(
                    os.path.join(
                        in_config.project_path(), "./data/output/sample_video/"
                    )
                ),
            ]
        )


class VideoToImagesCommand:

    # 	# Static member methods.
    def run(in_video_path, in_file_name, in_file_type, in_output):
        input_video_path = os.path.join(in_video_path)
        video_stream_handle = video_stream.VideoStream(input_video_path)

        if video_stream_handle is None:
            print(
                'Error : Could not open the video, to path = "'
                + input_video_path
                + '".'
            )
            return

        if not os.path.exists(in_output):
            print(
                'Warning : Path to output directory does not exist, creating the path = "'
                + in_output
                + '".'
            )
            os.makedirs(in_output)

        count: int = 0
        while True:
            frame = video_stream_handle.read()
            if frame is None:
                print("Status : Frame could not be read, exiting.")
                break

            path = os.path.join(
                in_output, in_file_name + str(count) + "." + in_file_type
            )
            cv2.imwrite(path, frame)
            count += 1

    def main(in_config, in_argv):
        print("Status : Start converting video to images.")

        arg_dict = ArgumentParser(
            in_config, VideoToImagesArgumentList(in_config), in_argv
        ).argument_dictionary

        path = None
        if "path" in arg_dict.keys():
            path = arg_dict["path"]

        name = None
        if "name" in arg_dict.keys():
            name = arg_dict["name"]

        type = None
        if "type" in arg_dict.keys():
            type = arg_dict["type"]

        output = None
        if "output" in arg_dict.keys():
            output = arg_dict["output"]

        VideoToImagesCommand.run(path, name, type, output)

        print("Status : End converting video to images.")
