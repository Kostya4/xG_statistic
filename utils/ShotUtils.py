import pandas as pd

TAG_MAPPER = {
    101: "Goal",
    1901: "IsCA",
    401: "Left",
    402: "Right",
    403: "Head/Body"
}

def convertFromJsonToSeries(shot):
    positionX = shot["positions"][0]["x"]
    positionY = shot["positions"][0]["y"]
    matchPeriod = shot["matchPeriod"]
    eventSec = shot["eventSec"]
    if matchPeriod == "1H":
        matchPeriod = 0.4
    else:
        matchPeriod = 0.6
    series = pd.Series((positionX, positionY, matchPeriod, eventSec, 0, 0, 0, 0, 0), index=["positionX", "positionY",
                                                                               "matchPeriod", "eventSec", "Goal",
                                                                               "Left", "Right", "Head/Body", "IsCA"])
    for tag in shot["tags"]:
        tagId = int(tag["id"])
        tagValue = TAG_MAPPER.get(tagId, 0)
        if tagValue != 0:
            series[tagValue] = 1

    return series


def convertAllShots(shots):
    result = []
    for shot in shots:
        convertedShot = convertFromJsonToSeries(shot)
        result.append(convertedShot)
    return result
