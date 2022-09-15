import abc

from mobile_robotics_python.messages import RobotStateMessage


class LocalisationSolutionBase(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "predict")
            and callable(subclass.predict)
            and hasattr(subclass, "update")
            and callable(subclass.update)
            or NotImplemented
        )

    @abc.abstractmethod
    def predict(self, stamp_s: float) -> RobotStateMessage:
        """Load in the data set"""
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, msg: RobotStateMessage) -> RobotStateMessage:
        """Extract text from the data set"""
        raise NotImplementedError
