import cv2

from enum import Enum


class EnumFeatureMatcher(Enum):
    E_FLANN_OpenCV = 1


class FeatureMatcherImplementationInterface:
    def compute(self, in_descriptor_1, in_descriptor_2):
        raise NotImplementedError("FeatureMatcherImplementationInterface::compute()")


class FlannBasedMatcherOpenCV(FeatureMatcherImplementationInterface):

    # 	# Python member method overides.
    def __init__(self):
        super().__init__()
        self.__m_instance = cv2.FlannBasedMatcher(
            dict(algorithm=0, trees=5), dict(checks=32)
        )

    # 	# Public member methods.
    def compute(self, in_descriptor_1, in_descriptor_2):
        return self.instance.knnMatch(in_descriptor_1, in_descriptor_2, k=2)

    # 	# Public setter and getter methods.
    @property
    def instance(self):
        return self.__m_instance

    @instance.setter
    def instance(self, in_value):
        self.__m_instance = in_value


class FeatureMatcher:

    # 	# Python member method overides.
    def __init__(
        self, in_enum_feature_matcher_implementation=EnumFeatureMatcher.E_FLANN_OpenCV
    ):
        self.__m_enum_feature_matcher_implementation = (
            in_enum_feature_matcher_implementation
        )

        self.__m_feature_matcher_implementation = (
            self.__get_feature_matcher_implementation(
                self.__m_enum_feature_matcher_implementation
            )()
        )

    # 	# Public member methods.
    def compute(self, in_descriptor_1, in_descriptor_2):
        feature_matches = None
        feature_matches = self.__m_feature_matcher_implementation.compute(
            in_descriptor_1, in_descriptor_2
        )
        return feature_matches

    def draw(self, in_frame, in_feature_points):
        return cv2.drawKeypoints(in_frame, in_feature_points, in_frame)

    # 	# Private member methods.
    def __get_feature_matcher_implementation(
        self, in_enum_feature_matcher_implementation: EnumFeatureMatcher
    ):
        # TODO : Switch to switch statement once on python 3.10
        return {EnumFeatureMatcher.E_FLANN_OpenCV: FlannBasedMatcherOpenCV}.get(
            in_enum_feature_matcher_implementation, FlannBasedMatcherOpenCV
        )
