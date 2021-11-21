from app.src.app_config import Config

from ap_vision.src.arguments.argument_list_interface import ArgumentListInterface

from ap_vision.src.arguments.path_argument import PathArgument
from ap_vision.src.arguments.file_type_argument import FileTypeArgument
from ap_vision.src.arguments.display_stream_argument import DisplayStreamArgument
from ap_vision.src.arguments.square_size_argument import SquareSizeArgument
from ap_vision.src.arguments.rows_argument import RowsArgument
from ap_vision.src.arguments.columns_argument import ColumnsArgument
from ap_vision.src.arguments.output_argument import OutputArgument


import os


class CalibrationArgumentList(ArgumentListInterface):
    
    # 	# Python member method overides.
    def __init__(self, in_config):
        super().__init__(
            [
                PathArgument(
                    os.path.join(in_config.project_path(), "./calibration/data/input/")
                ),
                DisplayStreamArgument(),
                FileTypeArgument(),
                SquareSizeArgument(),
                RowsArgument(),
                ColumnsArgument(),
                OutputArgument(os.path.join(in_config.project_path(), "./calibration/data/output/output.txt")),
            ]
        )
