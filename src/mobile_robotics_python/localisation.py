from .localisation_solutions.dead_reckoning import DeadReckoning
from .messages import RobotStateMessage


class Localisation:
    def __init__(self, config):
        self.name = config.name
        self.driver = config.driver
        self.parameters = config.parameters
        if self.driver == "dead_reckoning":
            self._impl = DeadReckoning(self.parameters)
        else:
            print(f"Unknown localisation solution {self.driver}")

    def predict(self, msg: RobotStateMessage) -> RobotStateMessage:
        return self._impl.predict(msg)

    def update(self, msg: RobotStateMessage) -> RobotStateMessage:
        return self._impl.update(msg)
