import abc
from mobile_robotics_python.messages import SpeedRequestMessage


class ActuatorDriverBase(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, "move") and callable(subclass.move) or NotImplemented

    @abc.abstractmethod
    def move(self, msg: SpeedRequestMessage):
        """Load in the data set"""
        raise NotImplementedError
