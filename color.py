#!encoding=utf-8
import colorsys


class Color:

    @staticmethod
    def rgb_to_hls(r, g, b):
        r, g, b = [x/255.0 for x in [r, g, b]]
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        return (h, l, s)

    @staticmethod
    def hls_to_rgb(h, l, s):
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return (r * 255, g * 255, b * 255)

    @staticmethod
    def getDifference(colorDict):
        totalDif = 0

        for key, value in colorDict.items():
            totalDif += abs(value[2] - value[1])

        return totalDif

    def __init__(self, minH, maxH, minL, maxL):
        self.minH = minH
        self.maxH = maxH
        self.minL = minL
        self.maxL = maxL
        # self.puntos = []
        self.qPoints = 0
        self.probability = 0
        self.squareCount = 0
        self.geneticPercentage = 0

    def matches(self, hlsColor):
        return hlsColor[0] >= self.minH and hlsColor[0] <= self.maxH and hlsColor[1] >= self.minL and hlsColor[1] <= self.maxL

    def incrementCount(self):
        self.qPoints += 1

    def setProbability(self, prob):
        self.probability = prob

    def increaseSquareCount(self, squareSize):
        self.squareCount += squareSize

    def decreaseSquareCount(self, squareSize):
        self.squareCount -= squareSize

    def resetSquareCount(self):
        self.squareCount = 0


def getColores():
    return {
        "black": Color(0, 1, 0, 0.11),
        "white": Color(0, 1, 0.95, 1),
        "red": Color(0, 0.07, 0, 1),
        "orange": Color(0.07, 0.14, 0, 1),
        "yellow": Color(0.14, 0.18, 0, 1),
        "green": Color(0.18, 0.44, 0, 1),
        "cyan": Color(0.44, 0.53, 0, 1),
        "blue": Color(0.53, 0.74, 0, 1),
        "purple": Color(0.74, 0.79, 0, 1),
        "pink": Color(0.79, 0.93, 0, 1),
        "red2": Color(0.93, 1, 0, 1)
    }

# if c < 25.0 or c[0] > 335.0 and c[0] < 360.0:
#                 nColors["Rojo"] = c
#             elif c[0] < 50.0:
#                 nColors["Naranja"] = c
#             elif c[0] < 65.0:
#                 nColors["Amarillo"] = c
#             elif c[0] < 160.0:
#                 nColors["Verde"] = c
#             elif c[0] < 190.0:
#                 nColors["Celeste"] = c
#             elif c[0] < 265.0:
#                 nColors["Azul"] = c
#             elif c[0] < 285.0:
#                 nColors["Morado"] = c
#             elif c[0] < 335.0:
#                 nColors["Rosado"] = c
#             elif c[1] < 11.0:
#                 nColors["Negro"] = c
#             elif c[1] > 95:
    # nColors["Blanco"] = c
