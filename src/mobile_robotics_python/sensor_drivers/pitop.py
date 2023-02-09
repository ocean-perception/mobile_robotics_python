import weakref

import numpy as np
import math
from pitop import EncoderMotor, ForwardDirection, Pitop
from pitop.pma.imu import IMU

from mobile_robotics_python import Console
from mobile_robotics_python.messages import RobotStateMessage
from mobile_robotics_python.tools.time import get_utc_stamp

from . import SensorDriverBase


class PiTopCompass(SensorDriverBase):
    def __init__(self, params, parent=None):
        if parent is not None:
            self._parent = weakref.ref(parent)
        self.ready = False
        try:
            self._imu = IMU()
            self.ready = True
        except Exception as e:
            Console.warn("    PiTopCompass could not be initialised. Error:", e)

    def read(self, robot_state: RobotStateMessage) -> RobotStateMessage:
        if not self.ready:
            Console.warn("    PiTopCompass is not ready")
            return RobotStateMessage()
        acc = self._imu.accelerometer
        gyro = self._imu.gyroscope
        ori = self._imu.orientation
        msg = RobotStateMessage()
        msg.stamp_s = get_utc_stamp()
        msg.roll_rad = np.radians(ori.roll)
        msg.pitch_rad = np.radians(ori.pitch)
        msg.yaw_rad = np.radians(ori.yaw)
        msg.wx_radps = np.radians(gyro.x)
        msg.wy_radps = np.radians(gyro.y)
        msg.wz_radps = np.radians(gyro.z)
        msg.ax_mpss = acc.x / 9.81
        msg.ay_mpss = acc.y / 9.81
        msg.az_mpss = acc.z / 9.81
        return msg


def create_encoder(params):
    try:
        motor = EncoderMotor(params["port"], ForwardDirection.CLOCKWISE)
        motor.wheel_diameter = params["wheel_diameter"]
        if params["invert"]:
            motor.forward_direction = ForwardDirection.COUNTER_CLOCKWISE
        return motor
    except Exception as e:
        Console.warn("    EncoderMotor could not be initialised. Error:", e)
        return None


class PiTopEncoder(SensorDriverBase):
    def __init__(self, params, parent=None):
        if parent is not None:
            self._parent = weakref.ref(parent)
        self._left_encoder = create_encoder(params["left"])
        self._right_encoder = create_encoder(params["right"])
        self.wheel_separation = params["wheel_separation"]

        self.ready = False
        if self._left_encoder is None or self._right_encoder is None:
            return
        self.previous_stamp = get_utc_stamp()
        self.previous_left = self._left_encoder.distance
        self.previous_right = self._right_encoder.distance
        self.ready = True

    def read(self, robot_state: RobotStateMessage) -> RobotStateMessage:
        if not self.ready:
            Console.warn("    PiTopEncoder is not ready")
            return RobotStateMessage()
        ts = get_utc_stamp()
        ld = self._left_encoder.distance
        rd = self._right_encoder.distance

        ts_diff = ts - self.previous_stamp
        l_diff = ld - self.previous_left
        r_diff = rd - self.previous_right

        left_wheel_speed = l_diff / ts_diff
        right_wheel_speed = r_diff / ts_diff
        linear_velocity = (right_wheel_speed + left_wheel_speed) / 2.0
        angular_velocity = (
            right_wheel_speed - left_wheel_speed
        ) / self.wheel_separation

        # Save for next iteration
        self.previous_stamp = ts
        self.previous_left = ld
        self.previous_right = rd

        msg = RobotStateMessage()
        msg.stamp_s = (ts + self.previous_stamp) / 2
        msg.vx_mps = linear_velocity * math.cos(robot_state.yaw_rad)
        msg.vy_mps = linear_velocity * math.sin(robot_state.yaw_rad)
        msg.wz_radps = angular_velocity
        return msg


class PiTopBattery(SensorDriverBase):
    def __init__(self, params, parent=None):
        if parent is not None:
            self._parent = weakref.ref(parent)
        self.ready = False
        try:
            self._battery = Pitop().battery
            self.ready = True
        except Exception as e:
            Console.warn("    PiTopBattery could not be initialised. Error:", e)

    def read(self, robot_state: RobotStateMessage):
        print(f"Battery capacity: {self._battery.capacity}")
        print(f"Battery time remaining: {self._battery.time_remaining}")
        print(f"Battery is charging: {self._battery.is_charging}")
        print(f"Battery is full: {self._battery.is_full}")
        print(f"Battery wattage: {self._battery.wattage}")


class PiTopScreen(SensorDriverBase):
    def __init__(self, params, parent=None):
        if parent is not None:
            self._parent = weakref.ref(parent)
        self.ready = False
        try:
            self._device = Pitop()
            self._display = self._device.miniscreen
            self.ready = True
        except Exception as e:
            Console.warn("    PiTopScreen could not be initialised. Error:", e)

    def read(self, robot_state: RobotStateMessage):
        print(f"Display brightness: {self._display.brightness}")
        print(f"Display blanking timeout: {self._display.blanking_timeout}")
        print(f"Display backlight is on: {self._display.backlight}")
        print(f"Display lid is open: {self._display.lid_is_open}")

    def print(self, msg):
        self._display.display_multiline_text(msg, font_size=20)

    def print_pixel_list(self, pixel_list: list):
        # Not implemented
        pass
