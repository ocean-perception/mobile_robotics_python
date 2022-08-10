import numpy as np
import yaml


class MissionControl:
    def __init__(self, mission_filename, missions_path):
        self.filename = missions_path / mission_filename
        if not self.filename.exists():
            raise FileNotFoundError(f"Mission file {self.filename} not found")
        data = yaml.safe_load(self.filename.open("r"))
        self.waypoints = np.array(data["waypoints"])
        self.current_waypoint = 0

    @property
    def waypoint(self):
        return self.waypoints[self.current_waypoint]

    def next(self):
        self.current_waypoint += 1
        if self.current_waypoint >= len(self.waypoints):
            self.current_waypoint = 0
        return self.waypoints[self.current_waypoint]

    @property
    def finished(self):
        return self.current_waypoint == len(self.waypoints)
