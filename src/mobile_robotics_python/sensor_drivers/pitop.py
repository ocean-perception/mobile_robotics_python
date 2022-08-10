from pitop import EncoderMotor, ForwardDirection, BrakingType
from pitop.pma.imu import IMU
from mobile_robotics_python.messages import RobotStateMessage, SpeedRequestMessage

from mobile_robotics_python.tools.time import get_utc_stamp

import numpy as np


class PiTopCompass:
    def __init__(self, params):
        self.ready = False
        try:
            self._imu = IMU()
            self.ready = True
        except Exception as e:
            print("    PiTopCompass could not be initialised. Error:", e)

    def read(self) -> RobotStateMessage:
        if not self.ready:
            return RobotStateMessage()
        acc = self._imu.accelerometer
        gyro = self._imu.gyroscope
        ori = self._imu.orientation
        msg = RobotStateMessage()
        msg.utc_stamp = get_utc_stamp()
        msg.roll_rad = ori.roll
        msg.pitch_rad = ori.pitch
        msg.yaw_rad = ori.yaw
        msg.wx_radps = gyro.x
        msg.wy_radps = gyro.y
        msg.wz_radps = gyro.z
        msg.ax_mpss = acc.x
        msg.ay_mpss = acc.y
        msg.az_mpss = acc.z
        return msg


def create_encoder(params):
    try:
        motor = EncoderMotor(params["port"], ForwardDirection.CLOCKWISE)
        motor.wheel_diameter = params["wheel_diameter"]
        if params["invert"]:
            motor.forward_direction = ForwardDirection.COUNTER_CLOCKWISE
        return motor
    except Exception as e:
        print("    EncoderMotor could not be initialised. Error:", e)
        return None


class PiTopEncoder:
    def __init__(self, params):
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

    def read(self) -> RobotStateMessage:
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
        msg.stamp_s = ts
        msg.vx_mps = linear_velocity
        msg.wz_radps = angular_velocity
        return msg
