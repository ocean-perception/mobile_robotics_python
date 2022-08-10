from typing import List
from dataclasses import dataclass, field

"""Empty message classes to agree on the message types.
"""


@dataclass
class LaserScanMessage:
    stamp_s: float = None  # acquisition time of the first ray in the scan.
    angle_min_rad: float = None  # start angle of the scan [rad]
    angle_max_rad: float = None  # end angle of the scan [rad]
    angle_increment_rad: float = None  # angular distance between measurements [rad]
    time_increment_s: float = None  # time between measurements [seconds]
    range_min_m: float = None  # minimum range value [m]
    range_max_m: float = None  # maximum range value [m]
    ranges: List[float] = field(default_factory=[])  # range data [m]
    # (Note: values < range_min or > range_max should be discarded)
    intensities: List[float] = field(
        default_factory=[]
    )  # intensity data [device-specific units]


@dataclass
class SpeedRequestMessage:
    stamp_s: float = None
    vx_mps: float = None
    vy_mps: float = None
    vz_mps: float = None
    wx_radps: float = None
    wy_radps: float = None
    wz_radps: float = None


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
