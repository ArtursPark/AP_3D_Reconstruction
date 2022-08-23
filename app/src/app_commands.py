from utility_apps.src.dlt import DirectLinearTransformCommand
from utility_apps.src.video_to_images import VideoToImagesCommand
from calibration.src.calibration_command import CalibrationCommand
from reconstruction.src.reconstruction_command import ReconstructionCommand


class AppCommands:
    """
    AppCommands class.
            This will contain the main commands for the various commands/apps/utilities.
    """

    # 	# Python member method overides.
    def __init__(self, in_config, in_command, in_argv):
        # Set up some private member variables.
        self.__m_argv = in_argv
        self.__m_config = in_config

        # Run the command.
        getattr(self, in_command)()

    # 	# Public member methods.
    def dlt(self):
        DirectLinearTransformCommand.main(self.__m_config, self.__m_argv[2:])

    def video_to_images(self):
        VideoToImagesCommand.main(self.__m_config, self.__m_argv[2:])

    def calibrate(self):
        CalibrationCommand.main(self.__m_config, self.__m_argv[2:])

    def reconstruction(self):
        ReconstructionCommand.main(self.__m_config, self.__m_argv[2:])
