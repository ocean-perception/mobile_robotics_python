from typing import Optional

from mobile_robotics_python.messages import RobotStateMessage


class DeadReckoning:
    def __init__(self, parameters, initial_state: Optional[RobotStateMessage] = None):
        """Initialise the dead reckoning algorithm.

        Parameters
        ----------
        parameters : dict
            Configuration parameters for the dead reckoning algorithm.
        initial_state : RobotStateMessage, optional
            Initial state, by default initialised to zeroes.
        """
        self.parameters = parameters
        if initial_state is None:
            self.state = RobotStateMessage()
            self.state.all_zero()
        else:
            self.state = initial_state

    def predict(self, stamp_s: float) -> RobotStateMessage:

        dt_s = stamp_s - self.state.stamp_s

        self.state.x_m = (
            self.state.x_m
            + self.state.vx_mps * dt_s
            + 0.5 * self.state.ax_mpss * dt_s**2
        )
        self.state.y_m = (
            self.state.y_m
            + self.state.vy_mps * dt_s
            + 0.5 * self.state.ay_mpss * dt_s**2
        )

        return self.state

    def update(self, msg: RobotStateMessage) -> RobotStateMessage:
        # TODO make this update generic for all fields
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
        if msg.wz_radps is not None:
            self.state.wz_radps = msg.wz_radps
        if msg.x_m is not None:
            self.state.x_m = msg.x_m
        if msg.y_m is not None:
            self.state.y_m = msg.y_m
        if msg.z_m is not None:
            self.state.z_m = msg.z_m
        if msg.vx_mps is not None:
            self.state.vx_mps = msg.vx_mps
        if msg.vy_mps is not None:
            self.state.vy_mps = msg.vy_mps
        if msg.vz_mps is not None:
            self.state.vz_mps = msg.vz_mps
        if msg.ax_mpss is not None:
            self.state.ax_mpss = msg.ax_mpss
        if msg.ay_mpss is not None:
            self.state.ay_mpss = msg.ay_mpss
        if msg.az_mpss is not None:
            self.state.az_mpss = msg.az_mpss
        return self.predict(msg.stamp_s)
