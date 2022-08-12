import argparse
import pathlib

from .configuration import Configuration
from .remote import SftpConnection, SshConnection
from .robot import Robot
from .tools import Console


def main():
    Console.banner()
    parser = argparse.ArgumentParser(description="Base code for mobile robotics")
    parser.add_argument("-c", "--configuration", help="Configuration file")
    parser.add_argument(
        "--upload", action="store_true", help="Upload current code to the robot"
    )
    parser.add_argument("--connect", action="store_true", help="Connect to the robot")

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Set the verbosity level"
    )
    args = parser.parse_args()

    if not args.configuration:
        Console.info("Please specify a configuration file")
        return

    if args.verbose:
        Console.set_verbosity(True)
    else:
        Console.set_verbosity(False)

    c = Configuration(args.configuration)

    if not args.upload and not args.connect:
        robot = Robot(c)
        robot.run()

    if args.upload:
        Console.info("Uploading the code to the robot")

        source_directory = pathlib.Path(__file__).parents[2].absolute()
        SftpConnection(c, source_directory)

    if args.connect:
        Console.info("Running the code in the robot")
        SshConnection(c)


if __name__ == "__main__":
    main()
