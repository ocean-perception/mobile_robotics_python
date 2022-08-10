from mobile_robotics_python.messages import SpeedRequestMessage, RobotStateMessage


class NaiveRotateMove:
    def __init__(self, parameters):
        self.parameters = parameters

    def compute_request(
        self, current_position: RobotStateMessage, desired_position: RobotStateMessage
    ) -> SpeedRequestMessage:
        msg = SpeedRequestMessage()
        return msg
