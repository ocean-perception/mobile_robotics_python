import weakref

from mobile_robotics_python import Console

from .messages import RobotStateMessage, SpeedRequestMessage
from .navigation_solutions.line_of_sight import LineOfSight
from .navigation_solutions.naive_rotate_move import NaiveRotateMove


class Navigation:
    def __init__(self, config, parent=None):
        if parent is not None:
            self._parent = weakref.ref(parent)
        self.name = config.name
        self.driver = config.driver
        self.parameters = config.parameters
        if self.driver == "naive_rotate_move":
            self._impl = NaiveRotateMove(self.parameters)
        elif self.driver == "line_of_sight":
            self._impl = LineOfSight(self.parameters)
        else:
            Console.error(f"Unknown localisation solution {self.driver}")

    def compute_request(
        self,
        current_position: RobotStateMessage,
        previous_waypoint: RobotStateMessage,
        next_waypoint: RobotStateMessage,
    ) -> SpeedRequestMessage:
        return self._impl.compute_request(
            current_position, previous_waypoint, next_waypoint
        )
