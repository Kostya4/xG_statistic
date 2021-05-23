import json

def loadJson(filePath):
    with open(filePath) as file:
        return json.load(file)
