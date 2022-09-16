from typing import Optional

from mobile_robotics_python.messages import RobotStateMessage

from . import LocalisationSolutionBase


class ExtendedKalmanFilter(LocalisationSolutionBase):
    def __init__(self, parameters, initial_state: Optional[RobotStateMessage] = None):
        """Initialise the algorithm.

        Parameters
        ----------
        parameters : dict
            Configuration parameters for the algorithm.
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
        # Your code starts here:

        # At the end of the function, return the predicted state
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
        # Your code starts here:

        # At the end of the function, return the updated state
        return self.state
