from dataclasses import dataclass
from .metadata import MetaData
from .bpm import Bpm
from .timescale import TimeScaleGroup
from .single import Single
from .slide import Slide, SlideStartPoint, SlideRelayPoint, SlideEndPoint
from .guide import Guide, GuidePoint


# 1tickをbeatに変換
tick1_beat = 4 / 1920

def _shift(note: Single | Slide | SlideStartPoint | SlideRelayPoint | SlideEndPoint | Guide | GuidePoint, beats: list[tuple]):
    if hasattr(note, "beat"):
        note_beat = round(note.beat, 10)
        key = (note_beat, int(note.lane - note.size + 8))
        if key in beats:
            note.beat += tick1_beat  # 1920分ずらす
            _shift(note, beats)
        else:
            beats.append(key)
    if hasattr(note, "connections"):
        for connection in note.connections:
            _shift(connection, beats)
    if hasattr(note, "midpoints"):
        for midpoint in note.midpoints:
            _shift(midpoint, beats)


@dataclass
class Score:
    metadata: MetaData
    notes: list[Bpm | TimeScaleGroup | Single | Slide | Guide]

    # 重なっているノーツをずらす
    def shift(self):
        notes = self.notes
        beats = []

        for note in notes:
            if isinstance(note, Bpm) or isinstance(note, TimeScaleGroup):
                continue
            _shift(note, beats)