import numpy as np

from mobile_robotics_python.messages import RobotStateMessage, SpeedRequestMessage
from mobile_robotics_python.tools.time import get_utc_stamp


class NaiveRotateMove:
    def __init__(self, parameters):
        self.parameters = parameters
        self.orientation_threshold = parameters["orientation_threshold"]
        self.position_threshold = parameters["position_threshold"]
        self.rotation_speed = parameters["rotation_speed"]
        self.linear_speed = parameters["linear_speed"]

    def compute_request(
        self, current_position: RobotStateMessage, desired_position: RobotStateMessage
    ) -> SpeedRequestMessage:

        diff_x = desired_position.x - current_position.x
        diff_y = desired_position.y - current_position.y
        desired_theta = np.arctan2(diff_y, diff_x)
        diff_theta = desired_theta - current_position.theta
        distance = (diff_x**2 + diff_y**2) ** 0.5

        msg = SpeedRequestMessage()
        msg.stamp_s = get_utc_stamp()
        if abs(diff_theta) > self.orientation_threshold:
            msg.wz_radps = self.rotation_speed * np.sign(diff_theta)
            return msg

        if distance > self.position_threshold:
            msg.vx_mps = self.linear_speed * np.sign(diff_x) * np.sign(diff_y)
            return msg
