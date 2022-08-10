from pathlib import Path

from pytransform3d.transform_manager import TransformManager

from .configuration import Configuration
from .localisation import Localisation
from .mission_control import MissionControl
from .motors import Motors
from .navigation import Navigation
from .sensors import Compass, Encoder, ExternalPositioning, Lidar
from .tools.rate import Rate


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

        # Create controllers
        self.localisation = Localisation(config.control.localisation)
        self.navigation = Navigation(config.control.navigation)
        self.mission_control = MissionControl(
            config.control.mission,
            Path(config.filename).parent / "missions",
            waypoint_threshold=0.1,
        )

        # Create motors
        self.motors = Motors(config.motors)

    def run(self):
        print("Running robot...")

        r = Rate(10.0)

        while not self.mission_control.finished:
            # Read sensors
            measurements = []
            if self.compass is not None:
                msg = self.compass.read()
                measurements.append(msg)
            if self.encoder is not None:
                msg = self.encoder.read()
                measurements.append(msg)

            # Update navigation
            for measurement in sorted(measurements, key=lambda m: m.stamp_s):
                self.state = self.localisation.update(measurement)

            #print("State", self.state)
            #print("current waypoint", self.mission_control.waypoint)
            print(self.mission_control.current_waypoint, self.state)

            self.mission_control.update(self.state)
            speed_request = self.navigation.compute_request(
                self.state, self.mission_control.waypoint
            )
            print("speed_request", speed_request)
            self.motors.move(speed_request)

            r.sleep()
