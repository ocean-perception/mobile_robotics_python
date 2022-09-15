from pathlib import Path

from .tools.pose import PoseManager

from .configuration import Configuration
from .localisation import Localisation
from .mission_control import MissionControl
from .motors import Motors
from .navigation import Navigation
from .sensors import Battery, Compass, Encoder, ExternalPositioning, Lidar, Screen
from .tools import Console
from .tools.rate import Rate


class Robot:
    def __init__(self, config: Configuration):
        Console.set_logging_file(config.logging_folder)

        self.poses = PoseManager()
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
            self.poses.add_transform(self.lidar.pose, "lidar")
        if config.sensors.compass is not None:
            self.compass = Compass(config.sensors.compass, config.logging_folder)
            self.poses.add_transform(self.compass.pose, "compass")
        if config.sensors.encoder is not None:
            self.encoder = Encoder(config.sensors.encoder, config.logging_folder)
            self.poses.add_transform(self.encoder.pose, "encoder")
        if config.sensors.external_positioning is not None:
            self.external_positioning = ExternalPositioning(
                config.sensors.external_positioning, config.logging_folder
            )
            self.poses.add_transform(
                self.external_positioning.pose, "external_positioning"
            )
        if config.sensors.battery is not None:
            self.battery = Battery(config.sensors.battery, config.logging_folder)
        if config.sensors.screen is not None:
            self.screen = Screen(config.sensors.screen, config.logging_folder)

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

        r = Rate(5.0)

        while not self.mission_control.finished:
            # Read sensors
            measurements = []
            if self.compass is not None:
                msg = self.compass.read(self.state)
                transform = self.poses.get_transform("compass")
                measurements.append((msg, transform, "compass"))
            if self.encoder is not None:
                msg = self.encoder.read(self.state)
                transform = self.poses.get_transform("encoder")
                measurements.append((msg, transform, "encoder"))
            if self.external_positioning is not None:
                msg = self.external_positioning.read(self.state)
                transform = self.poses.get_transform("external_positioning")
                measurements.append((msg, transform, "external_positioning"))
            if self.lidar is not None:
                msg = self.lidar.read(self.state)
                transform = self.poses.get_transform("lidar")
                measurements.append((msg, transform, "lidar"))

            # Update navigation
            if len(measurements) > 0:
                # Sort measurements by timestamp
                measurements.sort(key=lambda x: x[0].timestamp)
                for measurement in measurements:
                    measurement_value = measurement[0]
                    measurement_transform = measurement[1]
                    measurement_name = measurement[2]
                    self.state = self.localisation.update(measurement)

            self.mission_control.update(self.state)
            speed_request = self.navigation.compute_request(
                self.state, self.mission_control.waypoint
            )
            self.motors.move(speed_request)

            r.sleep()
