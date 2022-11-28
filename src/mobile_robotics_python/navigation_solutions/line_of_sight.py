import weakref

from mobile_robotics_python.messages import RobotStateMessage, SpeedRequestMessage

from . import NavigationSolutionBase


class LineOfSight(NavigationSolutionBase):
    def __init__(self, parameters, parent):
        """Initialise the algorithm.

        Parameters
        ----------
        parameters : dict
            Configuration parameters for the naive rotate move algorithm.
        """
        self.parameters = parameters
        if parent is not None:
            self._parent = weakref.ref(parent)

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
        # Your code starts here:
        msg = SpeedRequestMessage()
        # You will need to change the contents of this message with the required values

        # At the end of the function, return the speed request
        return msg
