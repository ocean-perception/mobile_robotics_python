import numpy as np
from .configuration import Configuration
from pytransform3d.transform_manager import TransformManager
from .sensors import Lidar, Compass, Encoder, ExternalPositioning


class Robot:
    def __init__(self, config: Configuration):
        self._tm = TransformManager()
        self._config = config

        print("Initializing robot", config.robot_name, "...")

        # Create empty sensors
        self.lidar = None
        self.compass = None
        self.encoder = None
        self.external_positioning = None

        # Check for sensors:
        if config.sensors.lidar is not None:
            self.lidar = Lidar(config.sensors.lidar)
        if config.sensors.compass is not None:
            self.compass = Compass(config.sensors.compass)
        if config.sensors.encoder is not None:
            self.encoder = Encoder(config.sensors.encoder)
        if config.sensors.external_positioning is not None:
            self.external_positioning = ExternalPositioning(
                config.sensors.external_positioning
            )
