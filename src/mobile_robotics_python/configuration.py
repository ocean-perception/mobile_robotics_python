import pprint
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import yaml
from pydantic import BaseModel

from mobile_robotics_python.tools.console import Console


class PoseDict(BaseModel):
    xyz: List[float]
    rpy: List[float]


class EntryWithParams(BaseModel):
    name: str
    driver: str
    parameters: Optional[dict] = None


class SensorConfiguration(EntryWithParams):
    pose: PoseDict


class SensorsConfiguration(BaseModel):
    lidar: Optional[SensorConfiguration] = None
    compass: Optional[SensorConfiguration] = None
    encoder: Optional[SensorConfiguration] = None
    external_positioning: Optional[SensorConfiguration] = None
    battery: Optional[EntryWithParams] = None
    screen: Optional[EntryWithParams] = None


class MissionConfiguration(BaseModel):
    name: str
    parameters: Optional[dict] = None


class ControlConfiguration(BaseModel):
    mission: MissionConfiguration
    localisation: EntryWithParams
    navigation: EntryWithParams


class RemoteConfiguration(BaseModel):
    ip: str
    username: str
    password: str
    upload_destination: str


class Configuration(BaseModel):
    robot_name: str
    remote: RemoteConfiguration
    sensors: SensorsConfiguration
    control: ControlConfiguration
    motors: EntryWithParams
    filename: str = None
    logging_folder: Optional[str] = None

    def __init__(self, filename):
        if not Path(filename).exists():
            raise FileNotFoundError(f"Configuration file {filename} not found")
        f = Path(filename).open("r")
        data = yaml.safe_load(f)
        super().__init__(**data)
        self.filename = filename
        self.logging_folder = Path(self.logging_folder)
        now = datetime.now()
        date_str = now.strftime("%Y%m%d_%H%M%S")
        self.logging_folder = self.logging_folder / date_str
        Console.info("Loaded valid configuration file")

    def print(self):
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(self.dict())
