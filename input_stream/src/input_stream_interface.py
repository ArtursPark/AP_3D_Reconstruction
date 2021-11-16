
class InputStreamInterface:
	"""
		Interface : InputStreamInterface class.

		Virtual methods :
			read()
			close()
	"""

	def read(self):
		raise NotImplementedError("InputStreamInterface::read()")

	def close(self):
		raise NotImplementedError("InputStreamInterface::close()")
	