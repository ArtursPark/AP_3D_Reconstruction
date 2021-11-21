class ArgumentInterface:
    """
    Interface : ArgumentInterface class
    """

    # 	# Python member method overides.
    def __init__(
        self,
        in_short_name,
        in_long_name,
        in_name,
        in_type,
        in_action,
        in_default_value,
        in_help,
    ):
        self.__m_short_name = in_short_name
        self.__m_long_name = in_long_name
        self.__m_name = in_name
        self.__m_type = in_type
        self.__m_action = in_action
        self.__m_default_value = in_default_value
        self.__m_help = in_help

        self.__m_value = self.__m_default_value

    # 	# Public member methods.
    def parse_argument_value(self, in_value):
        self.__m_value = in_value
        return self.__m_value

    # 	# Public setter and getter methods.
    @property
    def short_name(self):
        return self.__m_short_name

    @short_name.setter
    def short_name(self, in_value):
        self.__m_short_name = in_value

    @property
    def long_name(self):
        return self.__m_long_name

    @long_name.setter
    def long_name(self, in_value):
        self.__m_long_name = in_value

    @property
    def name(self):
        return self.__m_name

    @name.setter
    def name(self, in_value):
        self.__m_name = in_value

    @property
    def type(self):
        return self.__m_type

    @type.setter
    def type(self, in_value):
        self.__m_type = in_value

    @property
    def action(self):
        return self.__m_action

    @action.setter
    def action(self, in_value):
        self.__m_action = in_value

    @property
    def default_value(self):
        return self.__m_default_value

    @default_value.setter
    def default_value(self, in_value):
        self.__m_default_value = in_value

    @property
    def help(self):
        return self.__m_help

    @help.setter
    def help(self, in_value):
        self.__m_help = in_value

    @property
    def value(self):
        return self.__m_value

    @value.setter
    def value(self, in_value):
        self.__m_value = in_value
