import weakref

from mobile_robotics_python import Console

from .actuator_drivers.pololu_micromaestro import PololuMicroMaestro
from .configuration import EntryWithParams
from .messages import SpeedRequestMessage
from .sensors import BaseLoggable

try:
    from .actuator_drivers.pitop import PiTopMotors
except ImportError:
    pass


class Motors(BaseLoggable):
    def __init__(self, config: EntryWithParams, logging_folder: str, parent=None):
        super().__init__(
            config, logging_folder, parent=self, message_type="SpeedRequestMessage"
        )
        if parent is not None:
            self._parent = weakref.ref(parent)
        self.name = config.name
        self.driver = config.driver
        self.parameters = config.parameters
        self._impl = None
        if self.driver == "pitop_motors":
            Console.info("  * Adding motors:", self.name)
            self._impl = PiTopMotors(self.parameters, parent=self)
            return
        elif self.driver == "pololu_motors":
            Console.info("  * Adding motors:", self.name)
            self._impl = PololuMicroMaestro(self.parameters, parent=self)
            return
        else:
            Console.error(f"Unknown motors driver {self.driver}")
        self._impl.init(self.parameters)

    def move(self, msg: SpeedRequestMessage):
        msg = self._impl.move(msg)
        self.log(msg)
        return msg
