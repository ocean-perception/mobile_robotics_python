from mobile_robotics_python import Console

from .actuator_drivers.pitop import PiTopMotors
from .actuator_drivers.pololu_micromaestro import PololuMicroMaestro
from .configuration import EntryWithParams
from .messages import SpeedRequestMessage
from .sensors import BaseLoggable


class Motors(BaseLoggable):
    def __init__(self, config: EntryWithParams, logging_folder: str):
        super().__init__(config, logging_folder, message_type="SpeedRequestMessage")
        self.name = config.name
        self.driver = config.driver
        self.parameters = config.parameters
        if self.driver == "pitop_motors":
            self._impl = PiTopMotors(self.parameters)
        elif self.driver == "pololu_motors":
            self._impl = PololuMicroMaestro(self.parameters)
        else:
            print(f"Unknown motor driver {self.driver}")
        Console.info("  * Adding motors:", self.name)

    def move(self, msg: SpeedRequestMessage):
        msg = self._impl.move(msg)
        self.log(msg)
        return msg
