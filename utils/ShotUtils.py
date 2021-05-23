import pandas as pd

TAG_MAPPER = {
    101: "Goal",
    401: "Left",
    402: "Right",
    403: "Head/Body"
}

def convertFromJsonToSeries(shot):
    positionX = shot["positions"][0]["x"]
    positionY = shot["positions"][0]["y"]
    matchPeriod = shot["matchPeriod"]
    if matchPeriod == "1H":
        matchPeriod = 0
    else:
        matchPeriod = 1
    series = pd.Series((positionX, positionY, matchPeriod, 0, 0, 0, 0), index=["positionX", "positionY",
                                                                               "matchPeriod", "Goal",
                                                                               "Left", "Right", "Head/Body"])
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
