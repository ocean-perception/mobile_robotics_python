from pathlib import Path

from pytransform3d.transform_manager import TransformManager

from .configuration import Configuration
from .localisation import Localisation
from .mission_control import MissionControl
from .motors import Motors
from .navigation import Navigation
from .sensors import Compass, Encoder, ExternalPositioning, Lidar
from .tools import Console
from .tools.rate import Rate


class Robot:
    def __init__(self, config: Configuration):
        Console.set_logging_file(config.logging_folder)

        self._tm = TransformManager()
        self._config = config

        Console.info("Initializing robot", config.robot_name, "...")

        # Create empty sensors
        self.lidar = None
        self.compass = None
        self.encoder = None
        self.external_positioning = None

        # Check for sensors:
        if config.sensors.lidar is not None:
            self.lidar = Lidar(config.sensors.lidar, config.logging_folder)
        if config.sensors.compass is not None:
            self.compass = Compass(config.sensors.compass, config.logging_folder)
        if config.sensors.encoder is not None:
            self.encoder = Encoder(config.sensors.encoder, config.logging_folder)
        if config.sensors.external_positioning is not None:
            self.external_positioning = ExternalPositioning(
                config.sensors.external_positioning, config.logging_folder
            )

        # Create controllers
        self.localisation = Localisation(
            config.control.localisation, config.logging_folder
        )
        self.navigation = Navigation(config.control.navigation)
        self.mission_control = MissionControl(
            config.control.mission,
            Path(config.filename).parent / "missions",
        )

        # Create motors
        self.motors = Motors(config.motors, config.logging_folder)

    def run(self):
        Console.info("Running robot...")

        r = Rate(10.0)

        while not self.mission_control.finished:
            # Read sensors
            measurements = []
            if self.compass is not None:
                msg = self.compass.read()
                measurements.append(msg)
            if self.encoder is not None:
                self.encoder.yaw_rad = self.compass.yaw_rad
                msg = self.encoder.read()
                measurements.append(msg)

            # Update navigation
            for measurement in sorted(measurements, key=lambda m: m.stamp_s):
                self.state = self.localisation.update(measurement)

            # print("State", self.state)
            # print("current waypoint", self.mission_control.waypoint)
            self.mission_control.update(self.state)
            speed_request = self.navigation.compute_request(
                self.state, self.mission_control.waypoint
            )
            self.motors.move(speed_request)

            r.sleep()
