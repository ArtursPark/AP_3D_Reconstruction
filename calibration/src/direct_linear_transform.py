"""
	File name : direct_linear_transform.py
	File description : The direct linear transform implementations.
"""

from calibration.src.direct_linear_transform_interface import (
    DirectLinearTransformInterface,
)

import numpy
import typing


class DirectLinearTransform(DirectLinearTransformInterface):
    """DirectLinearTransform class.

    See ./documentation/my_notes/direct_linear_transform.pdf

    """

    # 	# Public global member variables.

    G_CONST_IMAGE_DIMENSION_SIZE = 2
    G_CONST_OBJECT_DIMENSION_SIZE = 3
    G_CONST_MINIMUM_NUMBER_OF_POINTS = 6

    # 	# Python member method overides.

    def __init__(self) -> None:
        super().__init__()

    # 	# Public virtual member method overides.

    def compute(
        self, in_image_points: numpy.ndarray, in_object_points: numpy.ndarray
    ) -> typing.Tuple[numpy.ndarray, numpy.double]:

        object_points = in_object_points
        image_points = in_image_points
        object_points_size = object_points.shape[0]

        # Validate input paramters.

        if image_points.shape[0] != object_points_size:
            raise ValueError(
                "The number of object points (%d) and image points (%d) is not the same."
                % (object_points_size, image_points.shape[0])
            )

        if image_points.shape[1] != DirectLinearTransform.G_CONST_IMAGE_DIMENSION_SIZE:
            raise ValueError(
                "Incorrect dimensions of the image points (%d) for DLT (it should be %d)."
                % (
                    image_points.shape[1],
                    DirectLinearTransform.G_CONST_IMAGE_DIMENSION_SIZE,
                )
            )

        if (
            object_points.shape[1]
            != DirectLinearTransform.G_CONST_OBJECT_DIMENSION_SIZE
        ):
            raise ValueError(
                "Incorrect dimensions of the object points (%d) for DLT (it should be %d)."
                % (
                    object_points.shape[1],
                    DirectLinearTransform.G_CONST_OBJECT_DIMENSION_SIZE,
                )
            )

        if object_points_size < DirectLinearTransform.G_CONST_MINIMUM_NUMBER_OF_POINTS:
            raise ValueError(
                "Direct Linear Transform requires at least %d points, number of points given is %d."
                % (
                    DirectLinearTransform.G_CONST_MINIMUM_NUMBER_OF_POINTS,
                    object_points_size,
                )
            )

        # Solve a set of linear equations Ax=b.
        # Step 1 : Build matrix A.

        big_a_matrix = self.__build_matrix_of_linear_equations(
            image_points, object_points
        )

        # Step 1.2 : Solve Ax=b using SVD.
        # We ignore the first 2 matrices and take the last column of the right singular vector. Then we normalize it.
        _, _, right_singular_vector = numpy.linalg.svd(big_a_matrix)
        projection_vector = right_singular_vector[-1, :] / right_singular_vector[-1, -1]

        # The parameters are in the last line of Vh and normalize them
        # Camera projection matrix
        projection_matrix = projection_vector.reshape(3, 4)

        # Step 2 : Compute the mean L2 distance between computed and true image points.
        error = self.__compute_error(
            in_image_points, in_object_points, projection_matrix
        )

        return projection_matrix, error

    def __build_matrix_of_linear_equations(
        self, in_image_points: numpy.ndarray, in_object_points: numpy.ndarray
    ) -> numpy.ndarray:
        """
                Build homogeneous system of linear equations using the known image, and object points.

                        Xi, Yi, Zi, are object 3D points.
                        xi, yi, zi, are image 2D points.
                        i, is a point number. As we do it for at least 6 points.

                        axi = [-Xi, -Yi, -Zi, -1, 0, 0, 0, 0, xi*Xi, xi*Yi, xi*Zi, xi]
                        ayi = [0, 0, 0, 0, -Xi, -Yi, -Zi, -1, yi*Xi, yi*Yi, yi*Zi, yi]

        Args:
                in_image_points (numpy.ndarray): Image points.
                in_object_points (numpy.ndarray): Object points.

        Returns:
                numpy.ndarray: Homogeneous system of linear equations.
        """

        if in_image_points.shape[0] != in_object_points.shape[0]:
            return None

        object_points_size = in_image_points.shape[0]

        big_a_matrix = list()

        for i in range(object_points_size):
            x_object = in_object_points[i, 0]
            y_object = in_object_points[i, 1]
            z_object = in_object_points[i, 2]

            x_image = in_image_points[i, 0]
            y_image = in_image_points[i, 1]

            big_a_matrix.append(
                [
                    -x_object,
                    -y_object,
                    -z_object,
                    -1,
                    0,
                    0,
                    0,
                    0,
                    x_image * x_object,
                    x_image * y_object,
                    x_image * z_object,
                    x_image,
                ]
            )
            big_a_matrix.append(
                [
                    0,
                    0,
                    0,
                    0,
                    -x_object,
                    -y_object,
                    -z_object,
                    -1,
                    y_image * x_object,
                    y_image * y_object,
                    y_image * z_object,
                    y_image,
                ]
            )

        big_a_matrix = numpy.asarray(big_a_matrix)

        return big_a_matrix

    def __compute_error(
        self,
        in_image_points: numpy.ndarray,
        in_object_points: numpy.ndarray,
        in_projection_matrix: numpy.ndarray,
    ) -> numpy.double:

        # Multiply every object point by the projection matrix.
        computed_homogenous_image_points = in_projection_matrix @ numpy.concatenate(
            (in_object_points.T, numpy.ones((1, in_object_points.shape[0])))
        )

        # Normalize image points.
        computed_normalized_image_points = (
            computed_homogenous_image_points / computed_homogenous_image_points[2, :]
        )

        # Mean L2 euclidean distance, from computed image points to true image points.
        mean_distance_error = numpy.sqrt(
            numpy.mean(
                numpy.sum(
                    (computed_normalized_image_points[0:2, :].T - in_image_points) ** 2,
                    1,
                )
            )
        )

        return mean_distance_error
