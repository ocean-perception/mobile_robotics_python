import numpy as np
from pytransform3d import rotations as pr
from pytransform3d import transformations as pt
from pytransform3d.transform_manager import TransformManager


class Pose:
    def __init__(self, frame_id, parent_frame_id=None):
        self.frame_id = frame_id
        self.parent_frame_id = parent_frame_id
        self._rpy = np.nan * np.ones(3)
        self._xyz = np.nan * np.ones(3)

    @property
    def x(self):
        return self._xyz[0]

    @property
    def y(self):
        return self._xyz[1]

    @property
    def z(self):
        return self._xyz[2]

    @property
    def roll(self):
        return self._rpy[0]

    @property
    def pitch(self):
        return self._rpy[1]

    @property
    def yaw(self):
        return self._rpy[2]

    @x.setter
    def x(self, x):
        self._xyz[0] = x

    @y.setter
    def y(self, y):
        self._xyz[1] = y

    @z.setter
    def z(self, z):
        self._xyz[2] = z

    @roll.setter
    def roll(self, roll):
        self._rpy[0] = roll

    @pitch.setter
    def pitch(self, pitch):
        self._rpy[1] = pitch

    @yaw.setter
    def yaw(self, yaw):
        self._rpy[2] = yaw

    def set_rpy(self, rpy):
        self._rpy = np.array([rpy[0], rpy[1], rpy[2]])

    def set_xyz(self, xyz):
        self._xyz = np.array([xyz[0], xyz[1], xyz[2]])

    def get_transform(self):
        return pt.transform_from(
            pr.active_matrix_from_intrinsic_euler_xyz(self._rpy), self._xyz
        )

    def from_transform(self, transform):
        self._xyz = transform[:3, -1]
        self._rpy = pr.intrinsic_euler_xyz_from_active_matrix(transform[0:3, 0:3])


class PoseManager:
    def __init__(self):
        self._tm = TransformManager()

    def add_transform(self, pose, frame_id, parent_frame_id="robot"):
        self._tm.add_transform(frame_id, parent_frame_id, pose.get_transform())

    def get_transform(self, frame_id, parent_frame_id="robot"):
        p = Pose(frame_id)
        p.from_transform(self._tm.get_transform(frame_id, parent_frame_id))
        return p
