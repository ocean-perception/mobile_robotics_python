import abc

from mobile_robotics_python.messages import SpeedRequestMessage


class ActuatorDriverBase(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        if cls is ActuatorDriverBase:
            return (
                hasattr(subclass, "move")
                and callable(subclass.move)
                and hasattr(subclass, "init")
                and callable(subclass.init)
                and hasattr(subclass, "name")
                and isinstance(subclass.name, str)
                and hasattr(subclass, "ready")
                and isinstance(subclass.ready, bool)
            )
        raise NotImplementedError

    @abc.abstractmethod
    def init(self, params: dict):
        """Init the class"""
        raise NotImplementedError

    @abc.abstractmethod
    def move(self, msg: SpeedRequestMessage):
        """Move the actuators"""
        raise NotImplementedError
