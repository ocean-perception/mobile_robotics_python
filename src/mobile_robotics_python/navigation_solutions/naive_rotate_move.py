import weakref

import numpy as np

from mobile_robotics_python.messages import RobotStateMessage, SpeedRequestMessage
from mobile_robotics_python.tools.time import get_utc_stamp

from . import NavigationSolutionBase


def sign_with_zero(value):
    """Returns the sign of the value, or 1 if the value is 0."""
    if value == 0:
        return 1
    elif value < 0:
        return -1
    elif value > 0:
        return 1

#def check_angle(desired ,current):
 #   if current <= np.pi:
  #      diff_theta = desired - current
   # if current > np.pi:
    #    diff_theta = desired - current + 2*np.pi
    #return diff_theta


class NaiveRotateMove(NavigationSolutionBase):
    def __init__(self, parameters, parent=None):
        """Initialise the naive rotate move algorithm.

        Parameters
        ----------
        parameters : dict
            Configuration parameters for the naive rotate move algorithm.
        """
        if parent is not None:
            self._parent = weakref.ref(parent)
        self.parameters = parameters
        self.orientation_threshold = parameters["orientation_threshold"]
        self.rotation_speed = parameters["rotation_speed"]
        self.linear_speed = parameters["linear_speed"]

    def compute_request(
        self,
        current_position: RobotStateMessage,
        previous_waypoint: RobotStateMessage,
        next_waypoint: RobotStateMessage,
    ) -> SpeedRequestMessage:
        """Computes the speed request to move from the current position to the desired position.

        Parameters
        ----------
        current_position : RobotStateMessage
            Current position.
        previous_waypoint : RobotStateMessage
            Previous waypoint.
        next_waypoint : RobotStateMessage
            Next waypoint.

        Returns
        -------
        SpeedRequestMessage
            Speed request.
        """
        diff_x = next_waypoint.x_m - current_position.x_m
        diff_y = next_waypoint.y_m - current_position.y_m
        desired_theta = np.arctan2(diff_y, diff_x)
        diff_theta = desired_theta - current_position.yaw_rad
        #print("----------------this the difference in angle 1 is -----------------", diff_theta)
        if diff_theta < -np.pi:
            diff_theta = diff_theta + 2*np.pi
        #print("----------------this the difference in angle 2 is -----------------", diff_theta)
        distance = (diff_x**2 + diff_y**2) ** 0.5
        msg = SpeedRequestMessage()
        msg.stamp_s = get_utc_stamp()
        msg.vx_mps = 0
        msg.wz_radps = 0
        if abs(diff_theta) > self.orientation_threshold:
            msg.wz_radps = self.rotation_speed * sign_with_zero(diff_theta)
            return msg
        if distance > 0:
            # Only move forward
            msg.vx_mps = self.linear_speed
            return msg
        return msg
