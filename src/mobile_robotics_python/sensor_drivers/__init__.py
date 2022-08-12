import abc


class SensorDriverBase(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, "read") and callable(subclass.read) or NotImplemented

    @abc.abstractmethod
    def read(self):
        """Read the sensor value"""
        raise NotImplementedError
