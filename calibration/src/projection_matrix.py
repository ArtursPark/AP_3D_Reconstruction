import numpy
import typing


class ProjectionMatrix:
    """ProjectionMatrix class.

    The class is for storing the projection matrix as well as allow for the projection matrix decomposition.

    """

    # 	# Public global member variables.
    
    G_CONST_ROTATION_FIX_MATRIX = numpy.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]])
    G_CONST_PROJECTION_VECTORIZE_SIZE = 11

    # 	# Python member method overides.
    
    def __init__(self, in_data: numpy.ndarray) -> None:
        self.__m_data = in_data

    # 	# Public member methods.

    def decompose(self) -> typing.Tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray]:
        """Decomposes the projection matrix into calibration matrix (K), rotation matrix (R), translation vector (T).

        Returns:
                Tuple[NDArray[3,3], NDArray[3,3], NDArray[3,1]]: K, R, T are returned inside a tuple.
        """
        # Step 1 : Split projection matrix, into intrinsic and extrinsic matrices.
        # P (projection matrix) = [ (H_3x3) | (h_3x1) ]

        big_h_matrix = self.data[:, :3]
        small_h_matrix = self.data[:, 3]

        # Inverse of the H matrix.
        inverse_big_h_matrix = numpy.linalg.inv(big_h_matrix)

        # Q, R = QR_Decomposition(H^-1)
        q_matrix, r_matrix = numpy.linalg.qr(inverse_big_h_matrix)

        # Step 2 : Get translation vector.
        # T/Xo (translation vector) = (-H^-1)(h)
        translation_matrix = numpy.dot(-inverse_big_h_matrix, small_h_matrix)

        # Step 3 : Get calibration matrix.
        # K (calibration/intrinsic matrix) = QR_Decomposition(H^-1).Q^-1
        homogenous_calibration_matrix = numpy.linalg.inv(r_matrix)
        calibration_matrix = (
            homogenous_calibration_matrix / homogenous_calibration_matrix[2, 2]
        )

        # Step 3.1 : Fix the signs on the diagonal of the calibration matrix. Additionally, because H is homogeneous, calibration is also homogeneous. So, we divide each element in the matrix by the
        # element in the last column, and row. This will result normalized calibration matrix.
        calibration_matrix = numpy.dot(
            calibration_matrix, ProjectionMatrix.G_CONST_ROTATION_FIX_MATRIX
        )

        # Step 4 : Get rotation matrix.
        # R (rotation matrix) = QR_Decomposition(H^-1).R^T
        rotation_matrix = q_matrix.T

        # Step 4.1 : We rotated the calibration matrix by 180 degrees, now we rotate the rotation matrix, too.
        rotation_matrix = numpy.dot(
            ProjectionMatrix.G_CONST_ROTATION_FIX_MATRIX, rotation_matrix
        )

        return calibration_matrix, rotation_matrix, translation_matrix

    def compose(
        self,
        in_calibration_matrix: numpy.ndarray,
        in_rotation_matrix: numpy.ndarray,
        in_translation_matrix: numpy.ndarray,
    ):
        """Composes a projection matrix from the input calibration, rotation and translation matrices.

                Computed using \"P = K * R * [ (I3x3) | - T ]\", where (I3x3) is a 3x3 identity matrix.

        Args:
                in_calibration_matrix (numpy.ndarray): Calibration matrix of size 3x3.
                in_rotation_matrix (numpy.ndarray): Rotation matrix of size 3x3.
                in_translation_matrix (numpy.ndarray): Translation matrix of size 3x1.
        """
        self.data = (
            in_calibration_matrix
            @ in_rotation_matrix
            @ (numpy.column_stack((numpy.eye(3), -in_translation_matrix)))
        )
        self.data = self.data / self.data[2, 3]

    def vectorize(self) -> numpy.ndarray:
        projection_vector = self.data[-1, :] / self.data[-1, -1]
        return projection_vector

    # 	# Public setter and getter methods.
    
    @property
    def data(self) -> numpy.ndarray:
        return self.__m_data

    @data.setter
    def data(self, in_data: numpy.ndarray):
        self.__m_data = in_data
