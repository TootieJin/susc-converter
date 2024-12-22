from dataclasses import dataclass, field
from typing import Literal


@dataclass
class GuidePoint:
    beat: float
    ease: Literal["in", "out", "linear"]
    lane: float
    size: float
    timeScaleGroup: float


@dataclass
class Guide:
    color: Literal["green", "yellow"]
    fade: Literal["in", "out"]
    midpoints: list = field(default_factory=list)
    type: str = "guide"

    def append(self, guidepoint: GuidePoint):
        self.midpoints.append(guidepoint)