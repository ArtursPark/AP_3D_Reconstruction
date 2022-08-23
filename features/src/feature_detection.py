import cv2

from enum import Enum


class EnumFeatureDetector(Enum):
    E_SIFT_OpenCV = 1


class FeatureDetectorImplementationInterface:
    def compute(self, in_frame):
        raise NotImplementedError("FeatureDetectorImplementationInterface::compute()")


class SIFTOpenCV(FeatureDetectorImplementationInterface):

    # 	# Python member method overides.
    def __init__(self):
        super().__init__()
        self.__m_instance = cv2.SIFT_create(nfeatures=20000)

    # 	# Public member methods.
    def compute(self, in_gray_frame):
        return self.instance.detectAndCompute(in_gray_frame, None)

    # 	# Public setter and getter methods.
    @property
    def instance(self):
        return self.__m_instance

    @instance.setter
    def instance(self, in_value):
        self.__m_instance = in_value


class FeatureDetector:

    # 	# Python member method overides.
    def __init__(
        self, in_enum_feature_detection_implementation=EnumFeatureDetector.E_SIFT_OpenCV
    ):
        self.__m_enum_feature_detection_implementation = (
            in_enum_feature_detection_implementation
        )

        self.__m_feature_detection_implementation = (
            self.__get_feature_detection_implementation(
                self.__m_enum_feature_detection_implementation
            )()
        )

    # 	# Public member methods.
    def compute(self, in_gray_frame):
        feature_points = None
        feature_descriptors = None
        (
            feature_points,
            feature_descriptors,
        ) = self.__m_feature_detection_implementation.compute(
            in_gray_frame,
        )
        return feature_points, feature_descriptors

    def draw(self, in_frame, in_feature_points):
        return cv2.drawKeypoints(in_frame, in_feature_points, in_frame)

    # 	# Private member methods.
    def __get_feature_detection_implementation(
        self, in_enum_feature_detection_implementation: EnumFeatureDetector
    ):
        """Obtains an appropriate implementation of the feature detection based on the EnumFeatureDetector enum.

        Args:
                        in_enum_feature_detection_implementation (EnumFeatureDetector): Enum, which points to one of the feature detection implementations.

        Returns:
                        FeatureDetectorImplementationInterface: Returns with respective object depending on input inheriting from FeatureDetectorImplementationInterface.
        """
        # TODO : Switch to switch statement once on python 3.10
        return {EnumFeatureDetector.E_SIFT_OpenCV: SIFTOpenCV}.get(
            in_enum_feature_detection_implementation, SIFTOpenCV
        )
