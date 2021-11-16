import numpy
import cv2

import glob
import os.path
import os


class Calibration:
	"""
	Calibration class.
			Implemented using Zhang's method with OpenCV.
	"""

	def __init__(
		self,
		in_image_dir_path: str,
		in_square_size: float,
		in_rows: int,
		in_columns: int,
		in_image_file_types_suffix: str = "jpg",
		in_output_path: str = "./data/output/output.txt",
		in_display_windows : bool = False
	):

		#   # Private member variables.
		self.__m_image_directory_path: str = in_image_dir_path
		self.__m_square_size: float = in_square_size
		self.__m_rows: int = in_rows
		self.__m_columns: int = in_columns
		self.__m_image_file_type_suffix: str = in_image_file_types_suffix
		self.__m_glob_search_string: str = (
			in_image_dir_path + "*." + in_image_file_types_suffix
		)
		self.__m_output_path: str = in_output_path
		self.__m_display_windows : bool = in_display_windows

	#   # Public methods.
	def run_calibration(self):

		# Set up windows
		cv2.namedWindow("Original Image", cv2.WINDOW_NORMAL)
		cv2.namedWindow("Calibration Image", cv2.WINDOW_NORMAL)
		cv2.namedWindow("Error Image", cv2.WINDOW_NORMAL)
		cv2.namedWindow("Corrected Image", cv2.WINDOW_NORMAL)

		# Set up calibration variables
		object_point = numpy.zeros(
			(self.columns * self.rows, 3),
			numpy.float32,
		)
		object_point[:, :2] = numpy.mgrid[0 : self.rows, 0 : self.columns].T.reshape(
			-1, 2
		)
		object_point = object_point * self.square_size

		object_points: list = list()  # 3D points in real world space
		image_points: list = list()  # 2D points in image plane

		# Find calibration frames
		image_files = glob.glob(self.glob_search_string)
		if not image_files:
			return False, "No images were found in path : " + self.glob_search_string

		# Get image size
		image_size = cv2.imread(image_files[0]).shape[:2]

		for image_file in image_files:

			# Check if image file exists
			if not os.path.isfile(image_file):
				continue

			image_original = cv2.imread(image_file)
			image = image_original.copy()
			image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

			found_corners, corners = self.__m_find_corners_on_chessboard(image_gray)
			found_draw, image_calibration = self.__m_draw_chessboard_corners(
				image, corners, found_corners
			)

			if found_corners and found_draw:
				object_points.append(object_point)
				image_points.append(corners)
			else:
				os.remove(image_file)

			cv2.imshow("Original Image", image_original)  # Show original image
			cv2.imshow("Calibration Image", image_calibration)  # Show calibration image
			if cv2.waitKey(1) & 0xFF == ord("q"):
				return

		camera_matrix, distortion_coefficients = self.__m_calibrate_camera(
			object_points, image_points, image_size
		)
		self.__m_save_calibration(camera_matrix, distortion_coefficients)

		for image_file in image_files:

			# Check if image file exists
			if not os.path.isfile(image_file):
				continue

			image_original = cv2.imread(image_file)
			image = image_original.copy()

			image_corrected = cv2.undistort(
				image, camera_matrix, distortion_coefficients
			)
			image_error = abs(image_original - image_corrected)

			# Display images
			cv2.imshow("Original Image", image_original)  # Show original image
			cv2.imshow("Error Image", image_error)  # Show error image
			cv2.imshow("Corrected Image", image_corrected)  # Show corrected image
			if cv2.waitKey(1) & 0xFF == ord("q"):
				return

	# 	# Static member methods.
	@staticmethod
	def load_calibration(in_path):
		file_handle = cv2.FileStorage(
			in_path,
			cv2.FILE_STORAGE_READ,
		)
		camera_matrix = file_handle.getNode("camera_matrix").mat()
		distortion_coefficients = file_handle.getNode("distortion_coefficients").mat()
		file_handle.release()
		return camera_matrix, distortion_coefficients

	#   # Public setter and getter methods.
	@property
	def image_directory_path(self):
		return self.__m_image_directory_path

	@image_directory_path.setter
	def image_directory_path(self, in_value):
		self.__m_image_directory_path = in_value

	@property
	def square_size(self):
		return self.__m_square_size

	@square_size.setter
	def square_size(self, in_value):
		self.__m_square_size = in_value

	@property
	def rows(self):
		return self.__m_rows

	@rows.setter
	def rows(self, in_value):
		self.__m_rows = in_value

	@property
	def columns(self):
		return self.__m_columns

	@columns.setter
	def columns(self, in_value):
		self.__m_columns = in_value

	@property
	def image_file_type_suffix(self):
		return self.__m_image_file_type_suffix

	@image_file_type_suffix.setter
	def image_file_type_suffix(self, in_value):
		self.__m_image_file_type_suffix = in_value

	@property
	def glob_search_string(self):
		return self.__m_glob_search_string

	@glob_search_string.setter
	def glob_search_string(self, in_value):
		self.__m_glob_search_string = in_value

	@property
	def output_path(self):
		return self.__m_output_path

	@output_path.setter
	def output_path(self, in_value):
		self.__m_output_path = in_value

	#   # Private member methods
	def __m_find_corners_on_chessboard(self, in_frame):

		found, corners = cv2.findChessboardCorners(
			in_frame,
			(self.rows, self.columns),
			None,
			cv2.CALIB_CB_ADAPTIVE_THRESH,
		)
		if found:
			criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
			corners = cv2.cornerSubPix(in_frame, corners, (11, 11), (-1, -1), criteria)
		return found, corners

	def __m_calibrate_camera(
		self, in_object_points, in_image_points, image_size=(0, 0)
	):
		ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
			in_object_points, in_image_points, image_size, None, None
		)
		return mtx, dist

	def __m_draw_chessboard_corners(self, frame, corners, in_found):

		return_value = in_found
		frame = cv2.drawChessboardCorners(
			frame,
			(self.rows, self.columns),
			corners,
			return_value,
		)
		return return_value, frame

	def __m_save_calibration(self, in_camera_matrix, in_distortion_coefficients):
		file_handle = cv2.FileStorage(
			self.output_path,
			cv2.FILE_STORAGE_WRITE,
		)
		file_handle.write("camera_matrix", in_camera_matrix)
		file_handle.write("distortion_coefficients", in_distortion_coefficients)
		file_handle.release()


