from mobile_robotics_python import Console

from .actuator_drivers.pololu_micromaestro import PololuMicroMaestro
from .configuration import EntryWithParams
from .messages import SpeedRequestMessage
from .sensors import BaseLoggable

class PiTopMotors:
    name = "pitop_motors"

try:
    from .actuator_drivers.pitop import PiTopMotors
except ImportError as e:
    pass


class Motors(BaseLoggable):
    def __init__(self, config: EntryWithParams, logging_folder: str):
        super().__init__(config, logging_folder, message_type="SpeedRequestMessage")
        self.name = config.name
        self.driver = config.driver
        self.parameters = config.parameters
        self._impl = None
        available_drivers = [PiTopMotors(), PololuMicroMaestro()]
        for driver in available_drivers:
            if driver.name == self.driver:
                Console.info("  * Adding motors:", self.name)
                driver.init(self.parameters)
                self._impl = driver
                return
        print(f"Unknown motor driver {self.driver}")

    def move(self, msg: SpeedRequestMessage):
        msg = self._impl.move(msg)
        self.log(msg)
        return msg
