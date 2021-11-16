"""
	File name : class_file_template.py
	File description : Copy this file whenever creating a new .py file. Use this as a base.
"""

# 	# Import my current project sources.

# 	# Import my other project packages.

# 	# Import 3rd party packages.

# 	# Import python core packages.


class ClassTemplate:
	"""
	Type : ClassTemplate class.
							Description.
	"""

	# 	# Private global member variables.
	G_CONST_VAR = None
	G_VAR = None

	# 	# Private global member variables.
	__m_private_var = None

	# 	# Python member method overides.
	def __init__(self):
		self.__m_template_member_var = None

	#	# Public virtual member method overides.

	# 	# Public member methods.
	def pub_member_func(self):
		pass

	# 	# Static member methods.
	def static_func():
		pass

	# 	# Public setter and getter methods.
	@property
	def template_member_var(self):
		return self.__m_template_member_var

	@template_member_var.setter
	def template_member_var(self, in_template_member_var):
		self.__m_template_member_var = in_template_member_var

	# 	# Private member methods.
	def __priv_member_func(self):
		pass


# 	# References :
#   # Description : Link
