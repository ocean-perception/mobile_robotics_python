from .configuration import EntryWithParams
from .actuator_drivers.pitop import PiTopMotors
from .messages import SpeedRequestMessage


class Motors:
    def __init__(self, config: EntryWithParams):
        self.name = config.name
        self.driver = config.driver
        self.parameters = config.parameters
        if self.driver == "pitop_motors":
            self._impl = PiTopMotors(self.parameters)
        else:
            print(f"Unknown motor driver {self.driver}")

    def move(self, msg: SpeedRequestMessage):
        return self._impl.move(msg)
