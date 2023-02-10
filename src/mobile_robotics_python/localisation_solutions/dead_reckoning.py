import weakref
from typing import Optional
import numpy as np

from mobile_robotics_python.messages import RobotStateMessage

from . import LocalisationSolutionBase


class DeadReckoning(LocalisationSolutionBase):
    def __init__(
        self, parameters, initial_state: Optional[RobotStateMessage] = None, parent=None
    ):
        """Initialise the dead reckoning algorithm.

        Parameters
        ----------
        parameters : dict
            Configuration parameters for the dead reckoning algorithm.
        initial_state : RobotStateMessage, optional
            Initial state, by default initialised to zeroes.
        """
        if parent is not None:
            self._parent = weakref.ref(parent)
        self.parameters = parameters
        if initial_state is None:
            self.state = RobotStateMessage()
            self.state.all_zero()
        else:
            self.state = initial_state

    def predict(self, stamp_s: float) -> RobotStateMessage:
        """Predicts the state at the given time stamp.

        Parameters
        ----------
        stamp_s : float
            Time stamp to predict the state at.

        Returns
        -------
        RobotStateMessage
            Predicted state.
        """
        dt_s = stamp_s - self.state.stamp_s
        self.state.stamp_s = stamp_s
        self.state.x_m = self.state.x_m + (self.state.vx_mps * np.cos(self.state.yaw_rad) - self.state.vy_mps * np.sin(self.state.yaw_rad) )* dt_s
        self.state.y_m = self.state.y_m + (self.state.vx_mps * np.sin(self.state.yaw_rad) + self.state.vy_mps * np.cos(self.state.yaw_rad) )* dt_s
        self.state.yaw_rad += self.state.wz_radps*dt_s
        return self.state

    def update(self, msg: RobotStateMessage) -> RobotStateMessage:
        """Updates the state with the given measurement message.

        Parameters
        ----------
        msg : RobotStateMessage
            Measurement message.

        Returns
        -------
        RobotStateMessage
            Updated state.
        """
        if msg.x_m is not None:
            self.state.x_m = msg.x_m
        if msg.y_m is not None:
            self.state.y_m = msg.y_m
        if msg.z_m is not None:
            self.state.z_m = msg.z_m
        if msg.roll_rad is not None:
            self.state.roll_rad = msg.roll_rad
        if msg.pitch_rad is not None:
            self.state.pitch_rad = msg.pitch_rad
        if msg.yaw_rad is not None:
            self.state.yaw_rad = msg.yaw_rad
        if msg.vx_mps is not None:
            self.state.vx_mps = msg.vx_mps
        if msg.vy_mps is not None:
            self.state.vy_mps = msg.vy_mps
        if msg.vz_mps is not None:
            self.state.vz_mps = msg.vz_mps
        if msg.wx_radps is not None:
            self.state.wx_radps = msg.wx_radps
        if msg.wy_radps is not None:
            self.state.wy_radps = msg.wy_radps
        if msg.wz_radps is not None:
            self.state.wz_radps = msg.wz_radps
        if msg.ax_mpss is not None:
            self.state.ax_mpss = msg.ax_mpss
        if msg.ay_mpss is not None:
            self.state.ay_mpss = msg.ay_mpss
        if msg.az_mpss is not None:
            self.state.az_mpss = msg.az_mpss
        return self.predict(msg.stamp_s)
