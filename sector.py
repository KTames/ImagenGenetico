from tipocolor import Color, getColores
import random
class Sector: 

    def __init__(self, logicX, logicY, minX, minY, maxX, maxY, probabilidad = 1):
        self.logicX = logicX
        self.logicY = logicY
        self.minX = minX
        self.maxX = maxX
        self.minY = minY
        self.maxY = maxY
        self.probabilidad = probabilidad
        self.points = []
        self._colors = getColores()
    
    def getColors(self):
        return self._colors

    def calculateColors(self):
        countPoints = len(self.points)
        if countPoints == 0:
            self._colors["white"].setProbability(1)
        else:
            qcolors = 0
            pointsToEvaluate = int(countPoints * (1. / 3.)) if countPoints > 500 else countPoints
            pointsToEvaluate = pointsToEvaluate if pointsToEvaluate < 500 else 500

            for pointIndex in range(0, pointsToEvaluate):
                rand = random.randint(0, countPoints - 1)

                point = self.points[rand]
                hls = Color.rgb_to_hls(point[0], point[1], point[2])

                for key, color in self._colors.items():
                    if color.matches(hls):
                        qcolors += 1
                        self._colors[key].incrementCount(point)
                        break
            
            for key, color in self._colors.items():
                self._colors[key].setProbability(color.qPoints / qcolors)


