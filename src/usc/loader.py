import json
from typing import TextIO
from src.notes.score import Score
from src.notes.metadata import MetaData
from src.notes.bpm import Bpm
from src.notes.timescale import TimeScaleGroup, TimeScalePoint
from src.notes.single import Single
from src.notes.slide import Slide, SlideStartPoint, SlideRelayPoint, SlideEndPoint
from src.notes.guide import Guide, GuidePoint


def load(fp: TextIO) -> Score:
    usc = json.load(fp)
    metadata = MetaData(
        title="",
        artist="",
        designer="",
        waveoffset=usc["usc"]["offset"]
    )

    notelist = []
    for obj in usc["usc"]["objects"]:
        type = obj["type"]

        if type == "bpm":
            notelist.append(
                Bpm(beat=obj["beat"], bpm=obj["bpm"])
            )

        elif type == "timeScaleGroup":
            group = TimeScaleGroup()
            for timescale in obj["changes"]:
                group.append(
                    TimeScalePoint(beat=timescale["beat"], timeScale=timescale["timeScale"])
                )
            notelist.append(group)

        elif type == "single":
            if "direction" in obj:
                notelist.append(
                    Single(
                        beat=obj["beat"], 
                        critical=obj["critical"],
                        lane=obj["lane"],
                        size=obj["size"],
                        timeScaleGroup=obj["timeScaleGroup"],
                        trace=obj["trace"],
                        direction=obj["direction"]
                    )
                )
            else:
                notelist.append(
                    Single(
                        beat=obj["beat"], 
                        critical=obj["critical"],
                        lane=obj["lane"],
                        size=obj["size"],
                        timeScaleGroup=obj["timeScaleGroup"],
                        trace=obj["trace"]
                    )
                )

        elif type == "slide":
            slide = Slide(critical=obj["critical"])
            for point in obj["connections"]:
                if point["type"] == "start":
                    slide.append(
                        SlideStartPoint(
                            beat=point["beat"], 
                            critical=point["critical"],
                            ease=point["ease"],
                            judgeType=point["judgeType"],
                            lane=point["lane"],
                            size=point["size"],
                            timeScaleGroup=point["timeScaleGroup"]
                        )
                    )
                elif point["type"] in ("tick", "attach"):
                    if "critical" in point:
                        slide.append(
                            SlideRelayPoint(
                                beat=point["beat"], 
                                ease=point["ease"],
                                lane=point["lane"],
                                size=point["size"],
                                timeScaleGroup=point["timeScaleGroup"] ,
                                type=point["type"],
                                critical=point["critical"]
                            )
                        )
                    else:
                        slide.append(
                            SlideRelayPoint(
                                beat=point["beat"], 
                                ease=point["ease"],
                                lane=point["lane"],
                                size=point["size"],
                                timeScaleGroup=point["timeScaleGroup"],
                                type=point["type"]
                            )
                        )
                elif point["type"] == "end":
                    if "direction" in point:
                        slide.append(
                            SlideEndPoint(
                                beat=point["beat"],
                                critical=point["critical"],
                                judgeType=point["judgeType"],
                                lane=point["lane"],
                                size=point["size"],
                                timeScaleGroup=point["timeScaleGroup"] ,
                                direction=point["direction"]
                            )
                        )
                    else:
                        slide.append(
                            SlideEndPoint(
                                beat=point["beat"],
                                critical=point["critical"],
                                judgeType=point["judgeType"],
                                lane=point["lane"],
                                size=point["size"],
                                timeScaleGroup=point["timeScaleGroup"]
                            )
                        )
            notelist.append(slide)

        elif type == "guide":
            guide = Guide(color=obj["color"], fade=obj["fade"])
            for point in obj["midpoints"]:
                guide.append(
                    GuidePoint(
                        beat=point["beat"],
                        ease=point["ease"],
                        lane=point["lane"],
                        size=point["size"],
                        timeScaleGroup=point["timeScaleGroup"]
                    )
                )
            notelist.append(guide)

    return Score(metadata=metadata, notes=notelist)