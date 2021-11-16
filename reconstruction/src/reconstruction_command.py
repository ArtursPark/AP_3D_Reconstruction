from reconstruction.src import reconstruction

from input_stream.src import video_stream
from input_stream.src import frame_stream
from input_stream.src import camera_stream

from input_stream.src import enum_input_stream
from reconstruction.src import enum_reconstruction
from reconstruction.src import reconstruction_arguments

class ReconstructionCommand:
	def main(argv):
		print("Status : Start reconstruction.")

		arg_dict = reconstruction_arguments.ArgumentParser(argv).argument_dictionary

		path = arg_dict["path"]

		stream = None
		if arg_dict["stream"] is enum_input_stream.EnumInputStream.E_VIDEO_STREAM:
			stream = video_stream.VideoStream(path)
		elif arg_dict["stream"] is enum_input_stream.EnumInputStream.E_FRAME_STREAM:
			stream = frame_stream.FrameStream(path)
		else:
			stream = camera_stream.CameraStream()

		calibration = arg_dict["calibration"]

		display_stream = False
		if enum_input_stream.EnumStreamDisplay.E_ON == arg_dict["display_stream"]:
			display_stream = True

		display_reconstruction = False
		if enum_reconstruction.EnumReconstructionPlotDisplay.E_ON == arg_dict["display_reconstruction"]:
			display_reconstruction = True	

		Reconstruction = reconstruction.Reconstruction(stream, calibration, display_stream, display_reconstruction)
		Reconstruction.compute()

		print("Status : End reconstruction.")