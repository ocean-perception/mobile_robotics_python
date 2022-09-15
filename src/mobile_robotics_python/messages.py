from dataclasses import dataclass, field
from typing import List

import numpy as np
import numpy.typing as npt

"""Empty message classes to agree on the message types.
"""

from mobile_robotics_python.tools.time import get_utc_stamp


@dataclass
class LaserScanMessage:
    stamp_s: float = None  # acquisition time of the first ray in the scan.
    angle_min_rad: float = None  # start angle of the scan [rad]
    angle_max_rad: float = None  # end angle of the scan [rad]
    time_increment_s: float = None  # time between measurements [seconds]
    range_min_m: float = None  # minimum range value [m]
    range_max_m: float = None  # maximum range value [m]
    ranges: List[float] = field(default_factory=list)  # range data [m]
    angles: List[float] = field(default_factory=list)  # angle data [m]
    # (Note: values < range_min or > range_max should be discarded)
    intensities: List[float] = field(
        default_factory=list
    )  # intensity data [device-specific units]

    def __post_init__(self):
        self.stamp_s = get_utc_stamp()


@dataclass
class SpeedRequestMessage:
    stamp_s: float = None
    vx_mps: float = None
    vy_mps: float = None
    vz_mps: float = None
    wx_radps: float = None
    wy_radps: float = None
    wz_radps: float = None

    def __post_init__(self):
        self.stamp_s = get_utc_stamp()


@dataclass
class RobotStateMessage:
    stamp_s: float = None  # acquisition time of the external positioning [seconds]
    x_m: float = None  # x position of the robot [m]
    y_m: float = None  # y position of the robot [m]
    z_m: float = None  # z position of the robot [m]
    roll_rad: float = None  # roll of the robot [rad]
    pitch_rad: float = None  # pitch of the robot [rad]
    yaw_rad: float = None  # yaw of the robot [rad]
    vx_mps: float = None  # linear velocity in x [m/s]
    vy_mps: float = None  # linear velocity in y [m/s]
    vz_mps: float = None  # linear velocity in z [m/s]
    wx_radps: float = None  # angular velocity in x [rad/s]
    wy_radps: float = None  # angular velocity in y [rad/s]
    wz_radps: float = None  # angular velocity in z [rad/s]
    ax_mpss: float = None  # linear acceleration in x [m/s^2]
    ay_mpss: float = None  # linear acceleration in y [m/s^2]
    az_mpss: float = None  # linear acceleration in z [m/s^2]
    covariance: npt.ArrayLike = None  # uncertainty of the state estimate

    def __post_init__(self):
        self.stamp_s = get_utc_stamp()

    def all_zero(self):
        self.x_m = 0
        self.y_m = 0
        self.z_m = 0
        self.roll_rad = 0
        self.pitch_rad = 0
        self.yaw_rad = 0
        self.vx_mps = 0
        self.vy_mps = 0
        self.vz_mps = 0
        self.wx_radps = 0
        self.wy_radps = 0
        self.wz_radps = 0
        self.ax_mpss = 0
        self.ay_mpss = 0
        self.az_mpss = 0
        self.covariance = np.zeros((15, 15))
