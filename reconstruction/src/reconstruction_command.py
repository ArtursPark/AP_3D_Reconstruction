from reconstruction.src.reconstruction import Reconstruction
from reconstruction.src.reconstruction_argument_list import ReconstructionArgumentList

from input_stream.src.video_stream import VideoStream
from input_stream.src.frame_stream import FrameStream
from input_stream.src.camera_stream import CameraStream

from ap_vision.src.arguments.argument_parser import ArgumentParser
from ap_vision.src.arguments.input_stream_argument import EnumInputStream


class ReconstructionCommand:
    def main(in_config, in_argv):
        print("Status : Start reconstruction.")

        arg_dict = ArgumentParser(
            in_config, ReconstructionArgumentList(in_config), in_argv
        ).argument_dictionary

        path = arg_dict["path"]

        stream = None
        if arg_dict["stream"] is EnumInputStream.E_VIDEO_STREAM:
            stream = VideoStream(path)
        elif arg_dict["stream"] is EnumInputStream.E_FRAME_STREAM:
            stream = FrameStream(path)
        else:
            stream = CameraStream()

        calibration = arg_dict["calibration"]
        display_stream = arg_dict["display_stream"]
        display_reconstruction = arg_dict["display_reconstruction"]

        reconstruction = Reconstruction(
            stream, calibration, display_stream, display_reconstruction
        )
        reconstruction.compute()

        print("Status : End reconstruction.")
