def retrieveId(shot):
    playerId = shot["playerId"]
    return playerId

def findById(id, players):
    for player in players:
        if id == int(player["passportArea"]["id"]):
            playerRole = player["role"]["name"]
            return playerRole
