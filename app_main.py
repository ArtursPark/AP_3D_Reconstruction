#   # Add current project modules.
import sys, os

# Add common packages.
sys.path.append(os.path.join(os.path.dirname(__file__), "common/package"))
# AP Vision common lib path.
sys.path.append(os.path.join(os.path.dirname(__file__), "common/package/ap_vision"))
# Camera calibration app path.
sys.path.append(os.path.join(os.path.dirname(__file__), "calibration"))

from app.src import application

#   # Set environment variables.
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"


def main():
    # Create the main app.
    app = application.ReconstructionApp.instance()
    # Parse the commands.
    app.parse_commands(sys.argv)
    # Run the command.
    app.run()
    # Close the app.
    app.close()


if __name__ == "__main__":
    main()
