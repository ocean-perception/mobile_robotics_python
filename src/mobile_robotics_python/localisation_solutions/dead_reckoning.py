from mobile_robotics_python.messages import RobotStateMessage
from typing import Optional


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
            self.state = RobotStateMessage().all_zero()
        else:
            self.state = initial_state

    def predict(self, stamp_s: float) -> RobotStateMessage:

        dt_s = stamp_s - self.state.stamp_s

        self.state.x_m = (
            self.state.x_m
            + self.state.vx_mps * dt_s
            + 0.5 * self.state.ax_mps * dt_s ** 2
        )
        self.state.y_m = (
            self.state.y_m
            + self.state.vy_mps * dt_s
            + 0.5 * self.state.ay_mps * dt_s ** 2
        )
        self.state.theta_rad = self.state.theta_rad + self.state.wz_radps * dt_s

        return self.state

    def update(self, msg: RobotStateMessage) -> RobotStateMessage:
        if msg.vx_mps is not None:
            self.state.vx_mps = msg.vx_mps
        if msg.vy_mps is not None:
            self.state.vy_mps = msg.vy_mps
        if msg.wz_radps is not None:
            self.state.wz_radps = msg.wz_radps
        return self.predict(msg.stamp_s)
