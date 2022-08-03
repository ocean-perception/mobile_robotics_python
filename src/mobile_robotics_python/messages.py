from typing import List
from dataclasses import dataclass

"""Empty message classes to agree on the message types.
"""


@dataclass(init=False)
class LaserScanMessage:
    stamp_s: float  # acquisition time of the first ray in the scan.
    angle_min_rad: float  # start angle of the scan [rad]
    angle_max_rad: float  # end angle of the scan [rad]
    angle_increment_rad: float  # angular distance between measurements [rad]
    time_increment_s: float  # time between measurements [seconds]
    range_min_m: float  # minimum range value [m]
    range_max_m: float  # maximum range value [m]
    ranges: List[
        float
    ]  # range data [m] (Note: values < range_min or > range_max should be discarded)
    intensities: List[float]  # intensity data [device-specific units]


@dataclass(init=False)
class CompassMessage:
    stamp_s: float  # acquisition time of the compass [seconds]
    heading_rad: float  # heading of the robot [rad]


@dataclass(init=False)
class ExternalPositioningMessage:
    stamp_s: float  # acquisition time of the external positioning [seconds]
    x_m: float  # x position of the robot [m]
    y_m: float  # y position of the robot [m]
    z_m: float  # z position of the robot [m]
    roll_rad: float  # roll of the robot [rad]
    pitch_rad: float  # pitch of the robot [rad]
    yaw_rad: float  # yaw of the robot [rad]


@dataclass(init=False)
class EncoderMessage:
    stamp_s: float  # acquisition time of the encoder [seconds]
    left_rad: float  # left wheel angular position [rad]
    right_rad: float  # right wheel angular position [rad]
