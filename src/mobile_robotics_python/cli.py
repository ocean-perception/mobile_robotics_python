import argparse

from .configuration import Configuration
from .robot import Robot
from .tools import Console


def main():
    Console.banner()
    parser = argparse.ArgumentParser(description="Base code for mobile robotics")
    parser.add_argument("-c", "--configuration", help="Configuration file")
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
    robot = Robot(c)
    robot.run()


if __name__ == "__main__":
    main()
