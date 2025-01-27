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

    def insert(self, index: int, time_scale: TimeScalePoint):
        self.changes.insert(index, time_scale)

    def get_sort_number(self) -> int:
        return 2