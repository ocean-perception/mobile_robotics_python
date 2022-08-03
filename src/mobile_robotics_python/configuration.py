import yaml
from pathlib import Path
from pydantic import BaseModel
from typing import Optional, List
import pprint


class PoseDict(BaseModel):
    xyz: List[float]
    rpy: List[float]


class SensorConfiguration(BaseModel):
    name: str
    driver: str
    parameters: Optional[dict] = None
    pose: PoseDict


class SensorsConfiguration(BaseModel):
    lidar: Optional[SensorConfiguration] = None
    compass: Optional[SensorConfiguration] = None
    encoder: Optional[SensorConfiguration] = None
    external_positioning: Optional[SensorConfiguration] = None


class MotorConfiguration(BaseModel):
    driver: str
    parameters: dict
    invert: bool


class MotorsConfiguration(BaseModel):
    left: MotorConfiguration
    right: MotorConfiguration


class Configuration(BaseModel):
    robot_name: str
    sensors: SensorsConfiguration
    motors: MotorsConfiguration

    def __init__(self, filename):
        if not Path(filename).exists():
            raise FileNotFoundError(f"Configuration file {filename} not found")
        f = Path(filename).open("r")
        data = yaml.safe_load(f)
        super().__init__(**data)
        print("Loaded valid configuration file")

    def print(self):
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(self.dict())
