import numpy as np
from pitop import EncoderMotor, ForwardDirection
from pitop.pma.imu import IMU

from mobile_robotics_python.messages import RobotStateMessage
from mobile_robotics_python.tools.time import get_utc_stamp


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
        if not self.ready:
            print("    PiTopEncoder is not ready")
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
        msg.stamp_s = ts
        msg.vx_mps = linear_velocity
        msg.wz_radps = angular_velocity
        return msg
