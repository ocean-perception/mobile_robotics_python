import abc

from mobile_robotics_python.messages import RobotStateMessage


class SensorDriverBase(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, "read") and callable(subclass.read) or NotImplemented

    @abc.abstractmethod
    def read(self, robot_state: RobotStateMessage):
        """Read the sensor value"""
        raise NotImplementedError
