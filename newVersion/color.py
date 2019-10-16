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

    def __init__(self, minH, maxH, minL, maxL, rgbColor):
        self.rgbColor = rgbColor
        self.minH = minH
        self.maxH = maxH
        self.minL = minL
        self.maxL = maxL
        self.qPoints = 0
        self.probability = 0
        self.squareCount = 0
        self.geneticPercentage = 0
        self.minBit = -1
        self.maxBit = -1
        self.target = 0

    def matches(self, hlsColor):
        return hlsColor[0] >= self.minH and hlsColor[0] <= self.maxH and hlsColor[1] >= self.minL and hlsColor[1] <= self.maxL

    def incrementCount(self):
        self.qPoints += 1

    def setProbability(self, prob):
        self.probability = prob

    def setBitBounds(self, min, max):
        self.minBit = min
        self.target = int(min + max / 2)
        self.maxBit = max
    
    def setMaxBound(self, max):
        self.maxBit = max
        self.target = int(self.minBit + max / 2)

    def matchesGenes(self, genes):
        return genes <= self.maxBit and genes >= self.minBit
        

    def increaseSquareCount(self):
        self.squareCount += 1

    def decreaseSquareCount(self):
        self.squareCount -= 1

    def resetSquareCount(self):
        self.squareCount = 0
        self.geneticPercentage = 0


def getColors():
    return {
        "black": Color(0, 1, 0, 0.11, (0, 0, 0)),
        "white": Color(0, 1, 0.97, 1, (255, 255, 255)),

        "red": Color(0, 0.07, 0.5, 1, (242, 13, 13)),
        "darkred": Color(0, 0.07, 0, 0.5, (97, 5, 5)),

        "orange": Color(0.07, 0.14, 0.5, 1, (244, 119, 42)),
        "darkorange": Color(0.07, 0.14, 0, 0.5, (111, 46, 6)),

        "yellow": Color(0.14, 0.18, 0.5, 1, (242, 215, 13)),
        "darkyellow": Color(0.14, 0.18, 0, 0.5, (121, 108, 6)),

        "green": Color(0.18, 0.44, 0.5, 1, (81, 255, 0)),
        "darkgreen": Color(0.18, 0.44, 0, 0.5, (37, 117, 0)),

        "cyan": Color(0.44, 0.53, 0.5, 1, (0, 255, 242)),
        "darkcyan": Color(0.44, 0.53, 0, 0.5, (0, 128, 121)),

        "blue": Color(0.53, 0.74, 0.5, 1, (5, 5, 255)),
        "darkblue": Color(0.53, 0.74, 0, 0.5, (0, 2, 128)),

        "purple": Color(0.74, 0.79, 0.5, 1, (94, 47, 202)),
        "darkpurple": Color(0.74, 0.79, 0, 0.5, (48, 24, 103)),

        "pink": Color(0.79, 0.93, 0.5, 1, (236, 0, 240)),
        "darkpink": Color(0.79, 0.93, 0, 0.5, (100, 0, 102)),

        "red2": Color(0.93, 1, 0, 1, (242, 13, 13)),
        "darkred2": Color(0.93, 1, 0, 1, (97, 5, 5)),
    }