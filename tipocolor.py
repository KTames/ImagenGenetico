import colorsys


class Color:
    qPoints = 0
    puntos = []
    probability = 0

    @staticmethod
    def rgb_to_hls(r, g, b):
        r, g, b = [x/255.0 for x in [r, g, b]]
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        return (h, l, s)

    def __init__(self, minH, maxH, minL, maxL):
        self.minH = minH
        self.maxH = maxH
        self.minL = minL
        self.maxL = maxL

    def matches(self, hslColor):
        return hslColor[0] >= self.minH and hslColor[0] <= self.maxH and hslColor[1] >= self.minL and hslColor[1] <= self.maxL

    def incrementCount(self, punto):
        self.puntos.append(punto)
        self.qPoints += 1

    def setProbability(self, prob):
        self.probability = prob


def getColores():
    return {
        "white": Color(0, 1, 0, 0.11),
        "black": Color(0, 1, 0.95, 1),
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
