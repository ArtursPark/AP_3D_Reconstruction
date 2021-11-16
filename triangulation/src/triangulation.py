import cv2

from enum import Enum


class EnumTriangulateImplementations(Enum):
    E_OpenCV = 1


class Triangulate:

    # 	# Python member method overides.
    def __init__(
        self, in_enum_triangulate_implementation=EnumTriangulateImplementations.E_OpenCV
    ):
        self.__m_enum_triangulate_implementation = in_enum_triangulate_implementation

        self.__m_triangulate_implementation = self.__get_triangulate_implementation(
            self.__m_enum_triangulate_implementation
        )

    # 	# Public member methods.
    def compute(
        self,
        in_previous_projection,
        in_current_projection,
        in_previous_points,
        in_current_points,
    ):

        homogenous_points = None
        homogenous_points = self.__m_triangulate_implementation(
            in_previous_projection,
            in_current_projection,
            in_previous_points,
            in_current_points,
        )

        if homogenous_points is None:
            return None

        if homogenous_points[0][0] != homogenous_points[0][0]:
            return None

        return homogenous_points

    # 	# Private member methods.
    def __triangulate_OpenCV(
        self,
        in_previous_projection,
        in_current_projection,
        in_previous_points,
        in_current_points,
    ):
        return cv2.triangulatePoints(
            in_previous_projection,
            in_current_projection,
            in_previous_points,
            in_current_points,
        )

    def __get_triangulate_implementation(self, in_enum_triangulate_implementation):
        # TODO : Switch to switch statement once on python 3.10
        return {EnumTriangulateImplementations.E_OpenCV: self.__triangulate_OpenCV}.get(
            in_enum_triangulate_implementation, self.__triangulate_OpenCV
        )
