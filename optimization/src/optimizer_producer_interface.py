from optimization.src.optimizer_data_interface import BundleAdjustmentData

import cv2
import numpy

class BundleAdjustmentProducerInterface:
	def __init__(self) -> None:
		self.__m_data = None

	def produce(self, in_frame_data) -> BundleAdjustmentData:
		raise NotImplementedError("OptimizerDataProducerInterface::produce()")


class BundleAdjustmentProducer(BundleAdjustmentProducerInterface):
	def __init__(self) -> None:
		super().__init__()

	def produce_paramater_array(in_stream_data, in_prev_frame_data, in_curr_frame_data, in_points):
		parameters = list()
  
		rotation_vector, _ = cv2.Rodrigues(in_prev_frame_data.rotation_matrix)
		parameters.append(rotation_vector[0])
		parameters.append(rotation_vector[1])
		parameters.append(rotation_vector[2])
		parameters.append(in_prev_frame_data.translation_matrix[0])
		parameters.append(in_prev_frame_data.translation_matrix[1])
		parameters.append(in_prev_frame_data.translation_matrix[2])
		parameters.append(in_stream_data.calibration_matrix[0])
		parameters.append(in_stream_data.distortion_coefficients[0])
		parameters.append(in_stream_data.distortion_coefficients[1])
  
		rotation_vector, _ = cv2.Rodrigues(in_curr_frame_data.rotation_matrix)
		parameters.append(rotation_vector[0])
		parameters.append(rotation_vector[1])
		parameters.append(rotation_vector[2])
		parameters.append(in_curr_frame_data.translation_matrix[0])
		parameters.append(in_curr_frame_data.translation_matrix[1])
		parameters.append(in_curr_frame_data.translation_matrix[2])
		parameters.append(in_stream_data.calibration_matrix[0])
		parameters.append(in_stream_data.distortion_coefficients[0])
		parameters.append(in_stream_data.distortion_coefficients[1])
  
		parameters = numpy.hstack((parameters, in_points))
		return parameters

	def produce(self, in_frame_data) -> BundleAdjustmentData:

		bundle_adjustment_data = BundleAdjustmentData()

		observation_count = 0
		frame_data_list = in_frame_data.frame_data_list
		zero_frame_data = frame_data_list[0]
		first_frame_data = frame_data_list[1]

		for match_1, match_2 in first_frame_data.feature_matches:
			if match_1.distance / match_2.distance < 0.75:

				bundle_adjustment_data.append(
					zero_frame_data.stream_id,
					0,
					observation_count,
					match_1.queryIdx,
				)

				bundle_adjustment_data.append(
					first_frame_data.stream_id,
					1,
					observation_count,
					match_1.trainIdx,
				)

				for i_index in range(2, len(frame_data_list)):

					ith_frame_data = frame_data_list[i_index]
					for new_match_1, new_match_2 in ith_frame_data.feature_matches:

						if (
							bundle_adjustment_data.point_index_list[-1]
							!= new_match_1.queryIdx
						):
							continue

						if new_match_1.distance / new_match_2.distance < 0.75:

							current_frame_data = frame_data_list[i_index]

							bundle_adjustment_data.append(
								current_frame_data.stream_id,
								i_index,
								observation_count,
								new_match_1.trainIdx,
							)

				observation_count += 1

		return bundle_adjustment_data

	def produce_local(
		self, in_previous_frame_data, in_current_frame_data
	) -> BundleAdjustmentData:

		bundle_adjustment_data = BundleAdjustmentData()

		observation_count = 0
		point_index = 0
		for match in in_current_frame_data.feature_matches:
			bundle_adjustment_data.append(
				in_current_frame_data.stream_id,
				0,
				observation_count,
				point_index,
				in_previous_frame_data.euclidean_object_points[:, match[0]],
				in_previous_frame_data.image_points[match[0]],
			)
			point_index += 1

			bundle_adjustment_data.append(
				in_current_frame_data.stream_id,
				1,
				observation_count,
				point_index,
				in_current_frame_data.euclidean_object_points[:, match[1]],
				in_current_frame_data.image_points[match[1]],
			)
			point_index += 1

			observation_count += 1

		return bundle_adjustment_data
