from mobile_robotics_python.messages import RobotStateMessage


class DeadReckoning:
    def __init__(self, parameters):
        self.parameters = parameters

    def predict(self, msg: RobotStateMessage) -> RobotStateMessage:
        msg = RobotStateMessage()
        return msg

    def update(self, msg: RobotStateMessage) -> RobotStateMessage:
        msg = RobotStateMessage()
        return msg
