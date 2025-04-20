from dataclasses import dataclass
from .metadata import MetaData
from .bpm import Bpm
from .timescale import TimeScaleGroup
from .single import Single
from .slide import Slide, SlideStartPoint, SlideRelayPoint, SlideEndPoint
from .guide import Guide, GuidePoint


# 1tickをbeatに変換
tick1_beat = round(4 / 1920, 6)

def _shift_slide(note: Slide | SlideStartPoint | SlideRelayPoint | SlideEndPoint | Guide | GuidePoint, beats: list[tuple], slide_beats: list):
    note_beat = round(note.beat, 6)
    key = (note_beat, int(note.lane - note.size + 8))
    if key in beats or note_beat in slide_beats:
        note.beat += tick1_beat  # 1920分ずらす
        _shift_slide(note, beats, slide_beats)
    else:
        beats.append(key)
        slide_beats.append(note_beat)

def _shift(note: Single | Slide | SlideStartPoint | SlideRelayPoint | SlideEndPoint | Guide | GuidePoint, beats: list[tuple]):
    if hasattr(note, "beat"):
        note_beat = round(note.beat, 6)
        key = (note_beat, int(note.lane - note.size + 8))
        if key in beats:
            note.beat += tick1_beat  # 1920分ずらす
            _shift(note, beats)
        else:
            beats.append(key)
    if hasattr(note, "connections"):
        connection_beats = []
        for connection in note.connections:
            _shift_slide(connection, beats, connection_beats)
    if hasattr(note, "midpoints"):
        midpoint_beats = []
        for midpoint in note.midpoints:
            _shift_slide(midpoint, beats, midpoint_beats)


@dataclass
class Score:
    metadata: MetaData
    notes: list[Bpm | TimeScaleGroup | Single | Slide | Guide]

    # フェードなしガイドの中継点を生成する
    def add_point_without_fade(self):
        notes = self.notes
        
        for note in notes:
            if not isinstance(note, Guide):
                continue
            if note.fade == "none":
                end_point = note.midpoints[-1]
                note.append(
                    GuidePoint(
                        beat=end_point.beat,
                        ease="linear",
                        lane=end_point.lane,
                        size=end_point.size,
                        timeScaleGroup=end_point.timeScaleGroup
                    )
                )

    # 重なっているノーツをずらす
    def shift(self):
        notes = self.notes
        beats = []

        for note in notes:
            if isinstance(note, Bpm) or isinstance(note, TimeScaleGroup):
                continue
            _shift(note, beats)