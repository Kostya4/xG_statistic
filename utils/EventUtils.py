def isShot(event):
    return event["eventName"] == "Shot"

def retrieveShotsFromEvents(events):
    return list(filter(isShot, events))
