import numpy as np
import yaml

from mobile_robotics_python.messages import RobotStateMessage


class MissionControl:
    def __init__(self, mission_filename, missions_path, waypoint_threshold=0.1):
        self.filename = missions_path / mission_filename
        if not self.filename.exists():
            raise FileNotFoundError(f"Mission file {self.filename} not found")
        data = yaml.safe_load(self.filename.open("r"))
        self.waypoints = np.array(data["waypoints"])
        self.current_waypoint = 0
        self.waypoint_threshold = waypoint_threshold

    def update(self, current_position: RobotStateMessage):
        """If the current position is close to the waypoint go to the next one."""
        diff_x = self.waypoint.x_m - current_position.x_m
        diff_y = self.waypoint.y_m - current_position.y_m
        distance = (diff_x**2 + diff_y**2) ** 0.5
        if distance < self.waypoint_threshold:
            self.next()

    @property
    def waypoint(self) -> RobotStateMessage:
        msg = RobotStateMessage()
        msg.x_m = self.waypoints[self.current_waypoint, 0]
        msg.y_m = self.waypoints[self.current_waypoint, 1]
        return msg

    def next(self):
        self.current_waypoint += 1
        if self.current_waypoint >= len(self.waypoints):
            self.current_waypoint = 0

    @property
    def finished(self):
        return self.current_waypoint == len(self.waypoints)
