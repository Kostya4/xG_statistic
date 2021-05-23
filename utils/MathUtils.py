import numpy as np

# todo: refactor this functions
def calculateShotDistance(x, y):
    return np.sqrt((105 - np.array(x)) ** 2 + (32.5 - np.array(y)) ** 2)

def calculateShotAngle(x, y):
    return np.arctan(((7.32 * (105 - np.array(x))) / ((105 - np.array(x)) ** 2 + (32.5 - np.array(y)) ** 2 - (7.32 / 2) ** 2)) * 180 / np.pi)
