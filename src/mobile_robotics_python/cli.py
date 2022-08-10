import argparse
from .configuration import Configuration
from .robot import Robot


def main():
    parser = argparse.ArgumentParser(description="Base code for mobile robotics")
    parser.add_argument("--version", action="version", version="1.0.0")
    parser.add_argument("-c", "--configuration", help="Configuration file")
    args = parser.parse_args()

    if not args.configuration:
        print("Please specify a configuration file")
        return

    c = Configuration(args.configuration)
    robot = Robot(c)
    robot.run()


if __name__ == "__main__":
    main()
