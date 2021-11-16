import cv2

class ViewFrame:

	# 	# Python member method overides.
	def __init__(self, in_window_name = "Default Window Name", in_close_key = "q", in_delay = 1):
		self.__m_window_name = in_window_name
		self.__m_close_key = in_close_key
		self.__m_delay = in_delay
		self.open()

    # 	# Public member methods.
	def open(self):
		cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)

	def close(self):
		cv2.destroyWindow(self.window_name)

	def view(self, in_frame):
		cv2.imshow(self.window_name, in_frame)
		return self.check_close_key()

	def check_close_key(self):
		key = cv2.waitKey(self.delay) & 0xFF
		if key == ord(self.close_key):
			return False
		return True

    # 	# Public setter and getter methods.
	@property
	def window_name(self):
		return self.__m_window_name

	@window_name.setter
	def window_name(self, in_value):
		self.__m_window_name = in_value  

	@property
	def close_key(self):
		return self.__m_close_key

	@close_key.setter
	def close_key(self, in_value):
		self.__m_close_key = in_value  

	@property
	def delay(self):
		return self.__m_delay

	@delay.setter
	def delay(self, in_value):
		self.__m_delay = in_value  