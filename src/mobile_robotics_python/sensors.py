from .tools.pose import Pose
from .configuration import SensorConfiguration
from .sensor_drivers.rplidar import RPLidar
from .sensor_drivers.pitop import PiTopCompass, PiTopEncoder
from .sensor_drivers.aruco_udp import ArUcoUDP
from .messages import LaserScanMessage, RobotStateMessage


class BaseTime:
    def __init__(self):
        self.time = 0.0

    def update(self, dt):
        self.time += dt


class BaseSensor:
    def __init__(self, config: SensorConfiguration):
        """Abstract class that defines the interface for all sensors.

        Parameters
        ----------
        config : SensorConfiguration
            Configuration for the sensor read from the YAML file
        """
        self.name = config.name
        self.driver = config.driver
        self.parameters = config.parameters
        self.pose = Pose(config.name)
        self.pose.set_xyz(config.pose.xyz)
        self.pose.set_rpy(config.pose.rpy)
        print("  * Adding sensor:", self.name)


class Lidar(BaseSensor):
    def __init__(self, config: SensorConfiguration):
        super().__init__(config)
        if self.driver == "rplidar":
            self._impl = RPLidar(self.parameters)
        else:
            print(f"Unknown lidar driver {self.driver}")

    def read(self) -> LaserScanMessage:
        return self._impl.read()


class Compass(BaseSensor):
    def __init__(self, config: SensorConfiguration):
        super().__init__(config)
        if self.driver == "pitop_compass":
            self._impl = PiTopCompass(self.parameters)
        else:
            print(f"Unknown compass driver {self.driver}")

    def read(self) -> RobotStateMessage:
        return self._impl.read()


class Encoder(BaseSensor):
    def __init__(self, config: SensorConfiguration):
        super().__init__(config)
        if self.driver == "pitop_encoder":
            self._impl = PiTopEncoder(self.parameters)
        else:
            print(f"Unknown encoder driver {self.driver}")

    def read(self) -> RobotStateMessage:
        return self._impl.read()


class ExternalPositioning(BaseSensor):
    def __init__(self, config: SensorConfiguration):
        super().__init__(config)
        if self.driver == "aruco_udp":
            self._impl = ArUcoUDP(self.parameters)
        else:
            print(f"Unknown compass driver {self.driver}")

    def read(self) -> RobotStateMessage:
        return self._impl.read()
