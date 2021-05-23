import numpy as np

# todo: refactor this functions
def calculateShotDistance(x, y):
    x_meter = x * 105 / 100
    y_meter = y * 68 / 100
    return np.sqrt((105 - np.array(x_meter)) ** 2 + (32.5 - np.array(y_meter)) ** 2)

def calculateShotAngle(x, y):
    x_meter = x * 105 / 100
    y_meter = y * 68 / 100
    return np.arctan(((7.32 * (105 - np.array(x_meter))) / ((105 - np.array(x_meter)) ** 2 + (32.5 - np.array(y_meter))
                                                            ** 2 - (7.32 / 2) ** 2)) * 180 / np.pi)
