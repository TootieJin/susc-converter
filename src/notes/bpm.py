from dataclasses import dataclass


@dataclass
class Bpm:
    beat: float
    bpm: float
    type: str = "bpm"