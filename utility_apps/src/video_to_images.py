"""
	File name : video_to_images.py
	File description : 
		This is a short and quick utility app that will split the video into a set of images and save them in output directory.
"""

from input_stream.src import video_stream

import cv2

import argparse
import os

class V2IsConfig:
	# 	# Public global member variables.
	# App details.
	G_CONST_APP_NAME : str = ""
	G_CONST_APP_DESCRIPTION : str = ""
	G_CONST_APP_PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

	# App argument details.
	G_ARGUMENT_VIDEO_PATH: str = ""
	G_CONST_ARGUMENT_VIDEO_PATH: str = "data/input/sample_video.mp4"
	G_CONST_HELP_VIDEO_PATH: str = ""

	G_ARGUMENT_IMAGE_NAME: str = ""
	G_CONST_ARGUMENT_IMAGE_NAME: str = "sample_image_"
	G_CONST_HELP_IMAGE_NAME: str = ""

	G_ARGUMENT_IMAGE_FILE_TYPE_SUFFIX: str = ""
	G_CONST_ARGUMENT_IMAGE_FILE_TYPE_SUFFIX: str = "jpg"
	G_CONST_HELP_IMAGE_FILE_TYPE_SUFFIX: str = ""

	G_ARGUMENT_OUTPUT_DIR: str = ""
	G_CONST_ARGUMENT_OUTPUT_DIR: str = "data/output/sample_video/"
	G_CONST_HELP_OUTPUT_DIR: str = ""


def argument_parser(in_argument_values):
	parser = argparse.ArgumentParser(
		prog=V2IsConfig.G_CONST_APP_NAME,
		description=V2IsConfig.G_CONST_APP_DESCRIPTION,
	)

	parser.add_argument(
		"-p",
		"--path",
		default=V2IsConfig.G_CONST_ARGUMENT_VIDEO_PATH,
		type=str,
		help=V2IsConfig.G_CONST_HELP_VIDEO_PATH,
	)

	parser.add_argument(
		"-i",
		"--image_name",
		default=V2IsConfig.G_CONST_ARGUMENT_IMAGE_NAME,
		type=str,
		help=V2IsConfig.G_CONST_HELP_IMAGE_NAME,
	)

	parser.add_argument(
		"-t",
		"--image_file_type",
		default=V2IsConfig.G_CONST_ARGUMENT_IMAGE_FILE_TYPE_SUFFIX,
		type=str,
		help=V2IsConfig.G_CONST_HELP_IMAGE_FILE_TYPE_SUFFIX,
	)

	parser.add_argument(
		"-o",
		"--output",
		default=V2IsConfig.G_CONST_ARGUMENT_OUTPUT_DIR,
		type=str,
		help=V2IsConfig.G_CONST_HELP_OUTPUT_DIR,
	)

	arguments = parser.parse_args(in_argument_values)

	V2IsConfig.G_ARGUMENT_VIDEO_PATH = arguments.path
	V2IsConfig.G_ARGUMENT_IMAGE_NAME = arguments.image_name
	V2IsConfig.G_ARGUMENT_IMAGE_FILE_TYPE_SUFFIX = arguments.image_file_type
	V2IsConfig.G_ARGUMENT_OUTPUT_DIR = arguments.output


def main(argv):

	argument_parser(argv)

	vpath = os.path.join(V2IsConfig.G_CONST_APP_PROJECT_PATH, V2IsConfig.G_ARGUMENT_VIDEO_PATH)
	vstream = video_stream.VideoStream(vpath)

	if vstream is None:
		print("ERROR : Could not open the video, to path = \"" + vpath + "\".")
		return

	if not os.path.exists(V2IsConfig.G_ARGUMENT_OUTPUT_DIR):
		print("WARNING : Path to output directory does not exist, creating the path = \"" + V2IsConfig.G_ARGUMENT_OUTPUT_DIR + "\".")
		os.makedirs(V2IsConfig.G_ARGUMENT_OUTPUT_DIR)
	
	count : int = 0
	while True:
		frame = vstream.read()
		if frame is None:
			print("STATUS : Frame could not be read, exiting.")
			break

		path = os.path.join(V2IsConfig.G_ARGUMENT_OUTPUT_DIR, V2IsConfig.G_ARGUMENT_IMAGE_NAME + str(count) + "." + V2IsConfig.G_ARGUMENT_IMAGE_FILE_TYPE_SUFFIX)
		cv2.imwrite(path, frame)
		count += 1