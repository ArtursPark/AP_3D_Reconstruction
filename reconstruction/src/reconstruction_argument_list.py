from app.src.app_config import Config

from ap_vision.src.arguments.argument_list_interface import ArgumentListInterface
from ap_vision.src.arguments.path_argument import PathArgument
from ap_vision.src.arguments.input_stream_argument import InputStreamArgument
from ap_vision.src.arguments.calibration_path_argument import CalibrationPathArgument
from ap_vision.src.arguments.display_stream_argument import DisplayStreamArgument
from ap_vision.src.arguments.display_reconstruction_argument import (
    DisplayReconstructionArgument,
)


class ReconstructionArgumentList(ArgumentListInterface):
    
	# 	# Python member method overides.
    def __init__(self, in_config):
        super().__init__(
            [
                PathArgument(),
                InputStreamArgument(),
                CalibrationPathArgument(in_config.project_path()),
                DisplayStreamArgument(),
                DisplayReconstructionArgument(),
            ]
        )
