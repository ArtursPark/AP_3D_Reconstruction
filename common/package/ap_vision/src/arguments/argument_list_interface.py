class ArgumentListInterface:
    """Interface : ArgumentListInterface class."""

    # 	# Python member method overides.
    def __init__(self, in_list):
        self.__m_list = in_list

        # 	# Public member methods.

    def create_dict(self, in_parsed_arguments):
        argument_dict = dict()
        for argument in self.list:
            value = argument.parse_argument_value(
                getattr(in_parsed_arguments, argument.name)
            )
            argument_dict[argument.name] = value
        return argument_dict

        # 	# Public setter and getter methods.

    @property
    def list(self):
        return self.__m_list

    @list.setter
    def list(self, in_value):
        self.__m_list = in_value
