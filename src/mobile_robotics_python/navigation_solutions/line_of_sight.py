from mobile_robotics_python.messages import RobotStateMessage, SpeedRequestMessage

from . import NavigationSolutionBase


class LineOfSight(NavigationSolutionBase):
    def __init__(self, parameters):
        """Initialise the algorithm.

        Parameters
        ----------
        parameters : dict
            Configuration parameters for the naive rotate move algorithm.
        """
        self.parameters = parameters

    def compute_request(
        self, current_position: RobotStateMessage, desired_position: RobotStateMessage
    ) -> SpeedRequestMessage:
        """Computes the speed request to move from the current position to the desired position.

        Parameters
        ----------
        current_position : RobotStateMessage
            Current position.
        desired_position : RobotStateMessage
            Desired position.

        Returns
        -------
        SpeedRequestMessage
            Speed request.
        """
        # Your code starts here:
        msg = SpeedRequestMessage()
        # You will need to change the contents of this message with the required values

        # At the end of the function, return the speed request
        return msg
