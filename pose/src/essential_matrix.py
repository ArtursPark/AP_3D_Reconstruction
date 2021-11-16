import cv2


class EssentialMatrix:
    """
    CalibrationMatrix class.
        Implemented using Zhang's method with OpenCV.
    """

    # 	# Public member methods.
    def compute(
        in_previous_points, in_current_points, in_intrinsic_matrix, in_method=cv2.RANSAC
    ):
        essential_matrix, mask = cv2.findEssentialMat(
            in_previous_points,
            in_current_points,
            in_intrinsic_matrix,
            in_method,
            0.999,
            1.0,
        )
        return essential_matrix, mask
