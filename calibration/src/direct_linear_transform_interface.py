"""
	File name : direct_linear_transform_interface.py
	File description : Interface for the direct linear transform.
"""

import numpy
import typing


class DirectLinearTransformInterface:
    """
    Interface : DirectLinearTransformInterface class.

            See ./documentation/my_notes/direct_linear_transform.pdf

    """

    # 	# Public virtual member methods.

    def compute(
        self, in_image_points: numpy.ndarray, in_object_points: numpy.ndarray
    ) -> typing.Tuple[numpy.ndarray, numpy.double]:
        raise NotImplementedError("DirectLinearTransformInterface::compute()")
