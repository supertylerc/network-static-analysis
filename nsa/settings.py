import os
from pathlib import Path

from ruamel.yaml import YAML


class Singleton(type):
    """Singleton metaclass for use later."""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(
                *args, **kwargs
            )
        return cls._instances[cls]


class Settings(metaclass=Singleton):
    """Settings singleton used throughout this project.

    Loads settings from ``settings.yaml`` by default.
    """

    def __init__(self):
        actual_path = self._get_path()
        yaml = YAML()
        with open(actual_path) as fhandle:
            settings = yaml.load(fhandle)
        for name, value in settings.items():
            setattr(self, name, value)

    def _get_path(self):
        possible_paths = [
            Path(os.getenv("NSA_FILE", "")),
            Path(Path.cwd() / "nsa.yml"),
            Path(Path.home() / ".nsa.yml"),
            Path(Path.cwd() / "nsa.yaml"),
            Path(Path.home() / ".nsa.yaml"),
        ]
        for path in possible_paths:
            if path.is_file():
                return path.resolve()

    @property
    def default_platform_patterns(self):
        return {
            "nxos": [r"Cisco Nexus Operating System \(NX-OS\) Software",],
            "iosxe": [r"IOS-XE Software",],
            "iosxr": [r"RP0/CPU0",],
            "junos": [
                r"JUNOS",
                # TC: Not 100% sure if this pattern is in other platforms
                #     It'll do for now until a bug is opened
                r"## Last commit: \d{4}-\d{2}-\d{2}.*by \w",
            ],
        }
