from .configuration import SensorConfiguration
from .messages import LaserScanMessage, RobotStateMessage, SpeedRequestMessage
from .sensor_drivers.aruco_udp import ArUcoUDP
from .sensor_drivers.qualisys import Qualisys
from .sensor_drivers.rplidar import RPLidar
from .sensor_drivers.sense_hat import SenseHatCompass, SenseHatScreen
from .tools import Console, Logger, Pose

try:
    from .sensor_drivers.pitop import (
        PiTopBattery,
        PiTopCompass,
        PiTopEncoder,
        PiTopScreen,
    )
except ImportError:
    pass

import weakref


class BaseLoggable:
    def __init__(
        self,
        config: SensorConfiguration,
        logging_folder: str,
        message_type="RobotStateMessage",
        parent=None,
    ):
        if parent is not None:
            self._parent = weakref.ref(parent)
        self.logger = Logger(config.name, logging_folder)
        self._message_type = message_type
        if message_type == "RobotStateMessage":
            self.logger.set_header(
                [
                    "sensor_stamp_s",
                    "x_m",
                    "y_m",
                    "z_m",
                    "roll_rad",
                    "pitch_rad",
                    "yaw_rad",
                    "vx_mps",
                    "vy_mps",
                    "vz_mps",
                    "wx_radps",
                    "wy_radps",
                    "wz_radps",
                    "ax_mpss",
                    "ay_mpss",
                    "az_mpss",
                ]
            )
        elif message_type == "SpeedRequestMessage":
            self.logger.set_header(
                [
                    "sensor_stamp_s",
                    "vx_mps",
                    "vy_mps",
                    "vz_mps",
                    "wx_radps",
                    "wy_radps",
                    "wz_radps",
                ]
            )
        elif message_type == "LaserScanMessage":
            self.logger.set_header(
                [
                    "stamp_s",
                    "angle_min_rad",
                    "angle_max_rad",
                    "time_increment_s",
                    "range_min_m",
                    "range_max_m",
                    "ranges",
                    "intensities",
                    "angles",
                ]
            )

    def log(self, msg):
        if msg is None:
            return
        if self._message_type == "RobotStateMessage":
            self.log_state(msg)
        elif self._message_type == "LaserScanMessage":
            self.log_scan(msg)
        elif self._message_type == "SpeedRequestMessage":
            self.log_velocity_request(msg)

    def log_state(self, msg: RobotStateMessage):
        """Log the sensor data to disk."""
        self.logger.log(
            msg.stamp_s,
            msg.x_m,
            msg.y_m,
            msg.z_m,
            msg.roll_rad,
            msg.pitch_rad,
            msg.yaw_rad,
            msg.vx_mps,
            msg.vy_mps,
            msg.vz_mps,
            msg.wx_radps,
            msg.wy_radps,
            msg.wz_radps,
            msg.ax_mpss,
            msg.ay_mpss,
            msg.az_mpss,
        )

    def log_scan(self, msg: LaserScanMessage):
        """Log the sensor data to disk."""
        self.logger.log(
            msg.stamp_s,
            msg.angle_min_rad,
            msg.angle_max_rad,
            msg.time_increment_s,
            msg.range_min_m,
            msg.range_max_m,
            str(msg.ranges),
            str(msg.intensities),
            str(msg.angles),
        )

    def log_velocity_request(self, msg: SpeedRequestMessage):
        """Log the sensor data to disk."""
        self.logger.log(
            msg.stamp_s,
            msg.vx_mps,
            msg.vy_mps,
            msg.vz_mps,
            msg.wx_radps,
            msg.wy_radps,
            msg.wz_radps,
        )


class BaseSensor(BaseLoggable):
    def __init__(
        self,
        config: SensorConfiguration,
        logging_folder: str,
        message_type="RobotStateMessage",
        has_pose=True,
        parent=None,
    ):
        """Abstract class that defines the interface for all sensors.

        Parameters
        ----------
        config : SensorConfiguration
            Configuration for the sensor read from the YAML file
        """
        super().__init__(config, logging_folder, parent=self, message_type=message_type)
        if parent is not None:
            self._parent = weakref.ref(parent)
        self.name = config.name
        self.driver = config.driver
        self.parameters = config.parameters
        self.pose = None
        if has_pose:
            self.pose = Pose(config.name)
            self.pose.set_xyz(config.pose.xyz)
            self.pose.set_rpy(config.pose.rpy)
        Console.info("  * Adding sensor:", self.name)


class Lidar(BaseSensor):
    def __init__(self, config: SensorConfiguration, logging_folder: str, parent=None):
        super().__init__(
            config, logging_folder, parent=self, message_type="LaserScanMessage"
        )
        if parent is not None:
            self._parent = weakref.ref(parent)
        if self.driver == "rplidar":
            self._impl = RPLidar(self.parameters)
        else:
            Console.error(f"Unknown lidar driver {self.driver}")

    def read(self, robot_state: RobotStateMessage) -> LaserScanMessage:
        msg = self._impl.read(robot_state)
        self.log(msg)
        return msg


class Compass(BaseSensor):
    def __init__(self, config: SensorConfiguration, logging_folder: str, parent=None):
        super().__init__(config, logging_folder, parent=self)
        if parent is not None:
            self._parent = weakref.ref(parent)
        if self.driver == "pitop_compass":
            self._impl = PiTopCompass(self.parameters, parent=parent)
        elif self.driver == "sensehat_compass":
            self._impl = SenseHatCompass(self.parameters, parent=parent)
        else:
            Console.error(f"Unknown compass driver {self.driver}")

    def read(self, robot_state: RobotStateMessage) -> RobotStateMessage:
        msg = self._impl.read(robot_state)
        self.log(msg)
        return msg


class Encoder(BaseSensor):
    def __init__(self, config: SensorConfiguration, logging_folder: str, parent=None):
        super().__init__(config, logging_folder, parent=self)
        if parent is not None:
            self._parent = weakref.ref(parent)
        if self.driver == "pitop_encoder":
            self._impl = PiTopEncoder(self.parameters)
        else:
            Console.error(f"Unknown encoder driver {self.driver}")

    def read(self, robot_state: RobotStateMessage) -> RobotStateMessage:
        msg = self._impl.read(robot_state)
        self.log(msg)
        return msg


class ExternalPositioning(BaseSensor):
    def __init__(self, config: SensorConfiguration, logging_folder: str, parent=None):
        super().__init__(config, logging_folder, parent=self)
        if parent is not None:
            self._parent = weakref.ref(parent)
        if self.driver == "aruco_udp":
            self._impl = ArUcoUDP(self.parameters)
        elif self.driver == "qualisys":
            self._impl = Qualisys(self.parameters)
        else:
            Console.error(f"Unknown compass driver {self.driver}")

    def read(self, robot_state: RobotStateMessage) -> RobotStateMessage:
        msg = self._impl.read(robot_state)
        self.log(msg)
        return msg


class Battery(BaseSensor):
    def __init__(self, config: SensorConfiguration, logging_folder: str, parent=None):
        super().__init__(config, logging_folder, parent=self, has_pose=False)
        if parent is not None:
            self._parent = weakref.ref(parent)
        if self.driver == "pitop_battery":
            self._impl = PiTopBattery(self.parameters)
        else:
            Console.error(f"Unknown compass driver {self.driver}")

    def read(self, robot_state: RobotStateMessage) -> RobotStateMessage:
        msg = self._impl.read(robot_state)
        self.log(msg)
        return msg


class Screen(BaseSensor):
    def __init__(self, config: SensorConfiguration, logging_folder: str, parent=None):
        super().__init__(config, logging_folder, parent=self, has_pose=False)
        if parent is not None:
            self._parent = weakref.ref(parent)
        if self.driver == "pitop_screen":
            self._impl = PiTopScreen(self.parameters)
        elif self.driver == "sensehat_screen":
            self._impl = SenseHatScreen(self.parameters)
        else:
            Console.error(f"Unknown compass driver {self.driver}")

    def read(self, robot_state: RobotStateMessage) -> RobotStateMessage:
        msg = self._impl.read(robot_state)
        self.log(msg)
        return msg

    def print(self, mgs: str):
        self._impl.print(mgs)

    def print_pixel_list(self, pixel_list: list):
        self._impl.print_pixel_list(pixel_list)
