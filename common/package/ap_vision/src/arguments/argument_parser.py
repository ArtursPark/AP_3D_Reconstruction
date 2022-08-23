from src.arguments.argument_list_interface import ArgumentListInterface

import argparse


class ArgumentParser:

    # 	# Python member method overides.
    def __init__(
        self,
        in_config,
        in_argument_list: ArgumentListInterface,
        in_argv,
        in_command_description=None,
        in_command_usage=None,
    ):

        command_description = in_config.app_description()
        if in_command_description is not None:
            command_description = in_command_description

        command_usage = in_config.app_usage()
        if in_command_usage is not None:
            command_usage = in_command_usage

        # Create the parser.
        self.__m_parser = argparse.ArgumentParser(
            prog=in_config.app_name(),
            description=command_description,
            usage=command_usage,
        )

        # List of arguments.
        self.__m_arg_list: ArgumentListInterface = in_argument_list

        # Add all arguments to the parser.
        for argument in self.__m_arg_list.list:
            self.__add_argument(self.__m_parser, argument)

        # Parse the arguments.
        parsed_arguments = self.__m_parser.parse_args(in_argv)

        # Create the argument to value dictionary.
        self.__m_argument_dictionary = self.__m_arg_list.create_dict(parsed_arguments)

    # 	# Public setter and getter methods.
    @property
    def argument_dictionary(self):
        return self.__m_argument_dictionary

    @argument_dictionary.setter
    def argument_dictionary(self, in_value):
        self.__m_argument_dictionary = in_value

    # 	# Private member methods.
    def __add_argument(self, in_parser, in_argument):
        if in_argument.action is None:
            in_parser.add_argument(
                in_argument.short_name,
                in_argument.long_name,
                default=in_argument.default_value,
                type=in_argument.type,
                help=in_argument.help,
            )
        else:
            in_parser.add_argument(
                in_argument.short_name,
                in_argument.long_name,
                default=in_argument.default_value,
                action=in_argument.action,
                help=in_argument.help,
            )
