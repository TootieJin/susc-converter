from dataclasses import dataclass, field


@dataclass
class TimeScalePoint:
    beat: float
    timeScale: float
        

@dataclass
class TimeScaleGroup:
    changes: list = field(default_factory=list)
    type: str = "timeScaleGroup"

    def append(self, time_scale: TimeScalePoint):
        self.changes.append(time_scale)