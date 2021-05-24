import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split

from utils import EventUtils
from utils import FileUtils
from utils import MathUtils
from utils import ShotUtils


def retrieveData():
    eventsFilePath = r'resources/events_Spain.json'

    events = FileUtils.loadJson(eventsFilePath)

    shots = EventUtils.retrieveShotsFromEvents(events)
    shots = ShotUtils.convertAllShots(shots)

    return pd.DataFrame(shots)


def main():
    data = retrieveData()

    goal = data[data["Goal"] == 1]
    noGoal = data[data["Goal"] == 0]
    noGoal = noGoal[:len(goal)]
    data = pd.DataFrame.append(goal, other=noGoal, ignore_index=True)

    positionX = data["positionX"]
    positionY = data["positionY"]

    distance = MathUtils.calculateShotDistance(positionX, positionY)
    data["distance"] = distance.tolist()

    angle = MathUtils.calculateShotAngle(positionX, positionY)
    data["angle"] = angle.tolist()

    data = data.drop(["positionX", "positionY"], axis=1)

    xTrain = data[["distance", "angle", "matchPeriod", "Left", "Right", "Head/Body"]]
    yTrain = data["Goal"]
    randomState = 12
    xTrain, xValidation, yTrain, yValidation = train_test_split(xTrain, yTrain, random_state=randomState)

    bestAccuracy = 0
    bestLearningRate = 0.0001
    learningRates = [0.0001, 0.001, 0.01, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    for learningRate in learningRates:
        gradientBoostingClassifier = GradientBoostingClassifier(learning_rate=learningRate)
        gradientBoostingClassifier.fit(xTrain, yTrain)

        print("Learning rate: ", learningRate)

        trainAccuracy = gradientBoostingClassifier.score(xTrain, yTrain)
        print("Accuracy score (training): {0:.3f}".format(trainAccuracy))

        testAccuracy = gradientBoostingClassifier.score(xValidation, yValidation)
        print("Accuracy score (validation): {0:.3f}".format(testAccuracy))

        if testAccuracy > bestAccuracy:
            bestAccuracy = testAccuracy
            bestLearningRate = learningRate

        predictions = gradientBoostingClassifier.predict(xValidation)
        print(predictions)

    print("Best learning rate: {}".format(bestLearningRate))
    print("Best accuracy: {0:.3f}".format(bestAccuracy))


if __name__ == "__main__":
    main()
