from mobile_robotics_python import Console

from .messages import RobotStateMessage, SpeedRequestMessage
from .navigation_solutions.naive_rotate_move import NaiveRotateMove


class Navigation:
    def __init__(self, config):
        self.name = config.name
        self.driver = config.driver
        self.parameters = config.parameters
        if self.driver == "naive_rotate_move":
            self._impl = NaiveRotateMove(self.parameters)
        else:
            Console.error(f"Unknown localisation solution {self.driver}")

    def compute_request(
        self, current_position: RobotStateMessage, desired_position: RobotStateMessage
    ) -> SpeedRequestMessage:
        return self._impl.compute_request(current_position, desired_position)
