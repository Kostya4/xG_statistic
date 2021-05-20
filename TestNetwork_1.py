import pandas as pd
import json
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.ensemble import GradientBoostingClassifier

COACHES_INPUT_FILE_PATH = r'Dataset\coaches.json'
COMPETITIONS_INPUT_FILE_PATH = r'E:\Student\Networks\Dataset\competitions.json'
PLAYERS_INPUT_FILE_PATH = r'E:\Student\Networks\Dataset\players.json'
REFEREES_INPUT_FILE_PATH = r'E:\Student\Networks\Dataset\referees.json'
TEAMS_INPUT_FILE_PATH = r'E:\Student\Networks\Dataset\teams.json'
MATCHES_SPAIN_INPUT_FILE_PATH = r'E:\Student\Networks\Dataset\matches_Spain.json'
EVENTS_SPAIN_INPUT_FILE_PATH = r'E:\Student\Networks\Dataset\events_Spain.json'
EVENTS_ITALY_INPUT_FILE_PATH = r'E:\Student\Networks\Dataset\events_Italy.json'
EVENTS_GERMANY_INPUT_FILE_PATH = r'E:\Student\Networks\Dataset\events_Germany.json'
EVENTS_ENGLAND_INPUT_FILE_PATH = r'E:\Student\Networks\Dataset\events_England.json'
EVENTS_FRANCE_INPUT_FILE_PATH = r'E:\Student\Networks\Dataset\events_France.json'
TAG_MAPPING = {101: "Goal", 401: "Left", 402: "Right", 403: "Head/Body"}


def loadJson(PathToFile):
    with open(PathToFile) as ptf:
        return json.load(ptf)


# spainEvents = loadJson(EVENTS_SPAIN_INPUT_FILE_PATH)
# spainEvents = list(filter(lambda event: event["eventName"] == "Shot", spainEvents))
# italyEvents = loadJson(EVENTS_ITALY_INPUT_FILE_PATH)
# italyEvents = list(filter(lambda event: event["eventName"] == "Shot", italyEvents))
# germanyEvents = loadJson(EVENTS_GERMANY_INPUT_FILE_PATH)
# germanyEvents = list(filter(lambda event: event["eventName"] == "Shot", germanyEvents))
englandEvents = loadJson(EVENTS_ENGLAND_INPUT_FILE_PATH)
shots = list(filter(lambda event: event["eventName"] == "Shot", englandEvents))
# italyEvents = loadJson(EVENTS_ITALY_INPUT_FILE_PATH)
# shots = list(filter(lambda event: event["eventName"] == "Shot", italyEvents))
players = loadJson(PLAYERS_INPUT_FILE_PATH)


def findById(id, players):
    for player in players:
        if id == int(player["passportArea"]["id"]):
            playerRole = player["role"]["name"]
            return playerRole


def retrieveId(shot):
    playerId = shot["playerId"]
    return playerId


def convertShot(shot):
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
        tagValue = TAG_MAPPING.get(tagId, 0)
        if tagValue != 0:
            series[tagValue] = 1

    return series


dataFrame = pd.DataFrame()
for shot in shots:
    # playerId = retrieveId(shot)
    # playerRole = findById(playerId, players)
    convertedShot = pd.DataFrame([convertShot(shot)])
    dataFrame = dataFrame.append(convertedShot, ignore_index=True)

x_meter = dataFrame[["positionX"]]
y_meter = dataFrame[["positionY"]]
distance = np.sqrt((105 - np.array(x_meter)) ** 2 + (32.5 - np.array(y_meter)) ** 2)
distance = pd.Series(distance, index="distance")
angle = np.arctan(
    ((7.32 * (105 - np.array(x_meter))) / ((105 - np.array(x_meter)) ** 2 + (32.5 - np.array(y_meter)) ** 2 -
                                           (7.32 / 2) ** 2)) * 180 / np.pi)
angle = pd.Series(angle, index="angle")
trainTestRatio = int(0.8 * dataFrame.shape[0])
train_data = dataFrame[:trainTestRatio]
test_data = dataFrame[trainTestRatio:]

y_train = train_data["Goal"]
train_data = train_data.drop("Goal", axis=1)

# scaler = MinMaxScaler()
# X_train = scaler.fit_transform(train_data[["positionX", "positionY"]])
# X_train = pd.DataFrame(X_train).merge(train_data[["matchPeriod", "Left", "Right", "Head/Body"]], left_index=True,
#                                      right_index=True)
# X_test = scaler.transform(test_data[["positionX", "positionY"]])
# X_test = pd.DataFrame(X_test).merge(test_data[["matchPeriod", "Left", "Right", "Head/Body"]], left_index=True,
#                                    right_index=True)

X_train = train_data[["matchPeriod", "Left", "Right", "Head/Body"]]
X_train = pd.DataFrame(X_train).merge(pd.Series([distance, angle], index=["distance", "angle"]),
                                      left_index=True, right_index=True)

state = 12

X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, random_state=state)

lr_list = [0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1]

for learning_rate in lr_list:
    gb_clf = GradientBoostingClassifier(n_estimators=20, learning_rate=learning_rate, max_features=2, max_depth=2,
                                        random_state=0)
    gb_clf.fit(X_train, y_train)

    # print("Learning rate: ", learning_rate)
    # print("Accuracy score (training): {0:.3f}".format(gb_clf.score(X_train, y_train)))
    # print("Accuracy score (validation): {0:.3f}".format(gb_clf.score(X_val, y_val)))
    predictions = gb_clf.predict(X_val)
    print(predictions, y_val)
# print("Confusion Matrix:")
# print(confusion_matrix(y_val, predictions))
# print("Classification Report")
# print(classification_report(y_val, predictions))
