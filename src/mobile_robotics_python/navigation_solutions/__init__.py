import abc

from mobile_robotics_python.messages import RobotStateMessage, SpeedRequestMessage


class NavigationSolutionBase(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "compute_request")
            and callable(subclass.compute_request)
            or NotImplemented
        )

    @abc.abstractmethod
    def compute_request(
        self, current_position: RobotStateMessage, desired_position: RobotStateMessage
    ) -> SpeedRequestMessage:
        """Extract text from the data set"""
        raise NotImplementedError
