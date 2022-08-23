from app.src import application
from app.src import app_commands

import argparse


class ParseCommands:
    """
    ParseCommands class.
    """

    #   # Private global member variables.
    __m_command_parser = None

    # 	# Python member method overides.
    def __init__(self, in_argv):

        if self.__m_command_parser is not None:
            return

        self.__m_command_parser = argparse.ArgumentParser(
            description=application.ReconstructionApp.G_APP_CONFIG.G_APP_DESCRIPTION,
            usage=application.ReconstructionApp.G_APP_CONFIG.G_APP_USAGE,
        )
        self.__m_command_parser.add_argument(
            "command", default="default", help="Command to execute."
        )

    # 	# Public member methods.
    def parse_commands(self, in_command):
        parsed_command = self.__m_command_parser.parse_args(in_command)
        if not hasattr(app_commands.AppCommands, parsed_command.command):
            self.__m_command_parser.print_help()
            exit(1)
        return parsed_command.command
