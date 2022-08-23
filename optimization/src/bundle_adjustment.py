# TODO : Implement bundle adjustment.

# TODO : Implement removal of outliers.
from __future__ import print_function

from optimization.src.optimizer_data_interface import BundleAdjustmentData

import bz2
import numpy as np
from scipy.sparse import lil_matrix
import matplotlib.pyplot as plt
import time
from scipy.optimize import least_squares
import cv2



def rotate(points, rot_vecs):
    """Rotate points by given rotation vectors.

    Rodrigues' rotation formula is used.
    """
    theta = np.linalg.norm(rot_vecs, axis=1)[:, np.newaxis]
    with np.errstate(invalid="ignore"):
        v = rot_vecs / theta
        v = np.nan_to_num(v)
    dot = np.sum(points * v, axis=1)[:, np.newaxis]
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)

    return (
        cos_theta * points + sin_theta * np.cross(v, points) + dot * (1 - cos_theta) * v
    )


def project(points, camera_params):
    """Convert 3-D points to 2-D by projecting onto images."""
    points_proj = rotate(points, camera_params[:, :3])
    points_proj += camera_params[:, 3:6]
    points_proj = -points_proj[:, :2] / points_proj[:, 2, np.newaxis]
    f = camera_params[:, 6]
    k1 = camera_params[:, 7]
    k2 = camera_params[:, 8]
    n = np.sum(points_proj ** 2, axis=1)
    r = 1 + k1 * n + k2 * n ** 2
    points_proj *= (r * f)[:, np.newaxis]
    return points_proj


def calc_fun(in_parameters, in_bundle_adjustment_data):
    """Compute residuals.

    `params` contains camera parameters and 3-D coordinates.
    """
    n_cameras = 2
    n_points = in_bundle_adjustment_data.point_list.size
    point_indices = in_bundle_adjustment_data.point_index_list
    camera_params = in_parameters[: n_cameras * 9].reshape((n_cameras, 9))
    points_3d = in_parameters[n_cameras * 9 :].reshape((n_points, 3))
    points_proj = project(points_3d[point_indices], camera_params[0])
    return (points_proj - in_bundle_adjustment_data.image_points).ravel()


def compute_residual_error(points_2d, re_projected_2d):
    """Compute residuals.

    `params` contains camera parameters and 3-D coordinates.
    """
    retvalue = (re_projected_2d - points_2d).ravel()
    return retvalue


def re_projection_points(in_frame_data, in_stream_data):

    rotation_vector, _ = cv2.Rodrigues(in_frame_data.rotation_matrix)
    re_projection_points, _ = cv2.projectPoints(
        in_frame_data.euclidean_object_points,
        rotation_vector,
        in_frame_data.translation_matrix,
        in_stream_data.calibration_matrix,
        in_stream_data.distortion_coefficients,
    )
    return re_projection_points


def compute_residual(
    in_optimization_parameters, in_bundle_adjustment_data: BundleAdjustmentData
):
    return re_projection_points(
        in_bundle_adjustment_data.frame_data, in_bundle_adjustment_data.stream_data
    )


def build_local_bundle_adjustment_jacobian(
    in_bundle_adjustment_data: BundleAdjustmentData,
):
    camera_indices = np.array(in_bundle_adjustment_data.camera_id_list)
    point_indices = np.array(in_bundle_adjustment_data.point_index_list)

    n_cameras = 2
    point_dim_size = 3
    pose_information_size = 9
    two_const = 2  # TODO : Figure out what this means.
    n_points = point_indices.size

    m = camera_indices.size * two_const
    n = n_cameras * pose_information_size + n_points * point_dim_size

    A_Jacobian = lil_matrix((m, n), dtype=int)

    index_cam_arr = np.arange(camera_indices.size)

    # Set camera parameters.
    for sub_mat in range(pose_information_size):
        A_Jacobian[
            two_const * index_cam_arr, camera_indices * pose_information_size + sub_mat
        ] = 1
        A_Jacobian[
            two_const * index_cam_arr + 1,
            camera_indices * pose_information_size + sub_mat,
        ] = 1

    # Set 3D object parameters in euclidean space.
    for sub_mat in range(point_dim_size):
        temp_x = two_const * index_cam_arr
        temp_y = (
            n_cameras * pose_information_size + point_indices * point_dim_size + sub_mat
        )
        A_Jacobian[
            temp_x,
            temp_y,
        ] = 1

        temp_x = two_const * index_cam_arr + 1
        temp_y = (
            n_cameras * pose_information_size + point_indices * point_dim_size + sub_mat
        )
        A_Jacobian[
            temp_x,
            temp_y,
        ] = 1

    return A_Jacobian
