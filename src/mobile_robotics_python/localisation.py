from mobile_robotics_python import Console

from .localisation_solutions.dead_reckoning import DeadReckoning
from .localisation_solutions.extended_kalman_filter import ExtendedKalmanFilter
from .localisation_solutions.particle_filter import ParticleFilter
from .localisation_solutions.slam import SLAM
from .messages import RobotStateMessage
from .sensors import BaseLoggable


class Localisation(BaseLoggable):
    def __init__(self, config, logging_folder):
        super().__init__(config, logging_folder, message_type="RobotStateMessage")
        self.name = config.name
        self.driver = config.driver
        self.parameters = config.parameters
        if self.driver == "dead_reckoning":
            self._impl = DeadReckoning(self.parameters)
        elif self.driver == "extended_kalman_filter":
            self._impl = ExtendedKalmanFilter(self.parameters)
        elif self.driver == "particle_filter":
            self._impl = ParticleFilter(self.parameters)
        elif self.driver == "slam":
            self._impl = SLAM(self.parameters)
        else:
            Console.error(f"Unknown localisation solution {self.driver}")

    def predict(self, msg: RobotStateMessage) -> RobotStateMessage:
        msg = self._impl.predict(msg)
        self.log(msg)
        return msg

    def update(self, msg: RobotStateMessage) -> RobotStateMessage:
        msg = self._impl.update(msg)
        self.log(msg)
        return msg
