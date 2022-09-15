from mobile_robotics_python import Console
from mobile_robotics_python.messages import RobotStateMessage

from . import SensorDriverBase
from .sense_hat_driver.sense_hat import SenseHat


class SenseHatCompass(SensorDriverBase):
    def __init__(self, params):
        self.ready = False
        try:
            self._dev = SenseHat()
            # Set IMU configuration:
            #   1) compass_enable = True
            #   2) gyro_enable = True
            #   3) accel_enable = True
            self._dev.set_imu_config(True, True, True)
            self.ready = True
        except Exception as e:
            Console.warn("    SenseHatCompass could not be initialised. Error:", e)

    def read(self, robot_state: RobotStateMessage) -> RobotStateMessage:
        if not self.ready:
            Console.warn("    SenseHatCompass is not ready")
            return RobotStateMessage()
        msg = RobotStateMessage()

        orientation_rad = self._dev.get_orientation_radians()
        accel_only = self._dev.get_accelerometer()
        gyro_only = self._dev.get_gyroscope()

        msg.roll_rad = orientation_rad["roll"]
        msg.pitch_rad = orientation_rad["pitch"]
        msg.yaw_rad = orientation_rad["yaw"]
        msg.wx_radps = gyro_only["roll"]
        msg.wy_radps = gyro_only["pitch"]
        msg.wz_radps = gyro_only["yaw"]
        msg.ax_mpss = accel_only["roll"]
        msg.ay_mpss = accel_only["pitch"]
        msg.az_mpss = accel_only["yaw"]

        return msg


class SenseHatScreen(SensorDriverBase):
    def __init__(self, params):
        self.ready = False
        try:
            self._dev = SenseHat()
            red = [255, 0, 0]  # Red
            blk = [0, 0, 0]  # Off
            # fmt: off
            question_mark = [
                blk, blk, blk, red, red, blk, blk, blk,
                blk, blk, red, blk, blk, red, blk, blk,
                blk, blk, blk, blk, blk, red, blk, blk,
                blk, blk, blk, blk, red, blk, blk, blk,
                blk, blk, blk, red, blk, blk, blk, blk,
                blk, blk, blk, red, blk, blk, blk, blk,
                blk, blk, blk, blk, blk, blk, blk, blk,
                blk, blk, blk, red, blk, blk, blk, blk]
            # fmt: on
            self.print_pixel_list(question_mark)
        except Exception as e:
            Console.warn("    SenseHatScreen could not be initialised. Error:", e)

    def read(self, robot_state: RobotStateMessage):
        # Not implemented
        pass

    def print(self, msg):
        """
        Scrolls a string of text across the LED matrix.
        """
        self._dev.show_message(msg)

    def print_pixel_list(self, pixel_list):
        """
        Accepts a list containing 64 smaller lists of [R,G,B] pixels and
        updates the LED matrix. R,G,B elements must intergers between 0
        and 255.
        """
        self._dev.set_pixels(pixel_list)
