#!encoding=utf-8
from color import Color, getColores
import random
from square import Square

class Sector:

    def __init__(self, logicX, logicY, minX, minY, maxX, maxY):
        self.logicX = logicX
        self.logicY = logicY
        self.minX = minX
        self.maxX = maxX
        self.minY = minY
        self.maxY = maxY
        self.probabilidad = 1
        self.points = []
        self._colors = getColores()
        self.generations = [[]]
        self.size = maxX - minX

    def getColors(self):
        return self._colors

    def calculateColors(self):
        """
            Calcula los porcentajes de color de los puntos que se eligieron en el probabilista
        """
        countPoints = len(self.points)
        if countPoints == 0:
            self._colors["white"].setProbability(1)

        else:
            qcolors = 0

            pointsToEvaluate = int(
                countPoints * (1. / 3.)
            )if countPoints > 500 else countPoints

            pointsToEvaluate = pointsToEvaluate if pointsToEvaluate < 500 else 500

            for pointIndex in range(0, pointsToEvaluate):
                rand = random.randint(0, countPoints - 1)

                point = self.points[rand]
                hls = Color.rgb_to_hls(point[0], point[1], point[2])

                for key, color in self._colors.items():
                    if color.matches(hls):
                        qcolors += 1
                        self._colors[key].incrementCount()
                        break

            for key, color in self._colors.items():
                self._colors[key].setProbability(color.qPoints / qcolors)

        self._createFirstGeneration()

    def _createFirstGeneration(self):
        # Se crean 3 cuadrados iniciales. Esto para que queden 2 padres elegibles y 1 no elegible.
        # Si hubieran sólo 2 cuadrados iniciales, quedaría 1 no elegible y sólo 1 elegible, lo cual no puede pasar
        for index in range(0, 3):
            rand = random.randint(1, 100) / 100

            selectedColor = None
            selectedKey = ""
            for key, color in self._colors.items():
                selectedColor = color
                selectedKey = key
                rand -= color.probability
                if rand <= 0:
                    break

            h = random.randint(int(selectedColor.minH * 100), int(selectedColor.maxH * 100)) / 100
            l = random.randint(int(selectedColor.minL * 100), int(selectedColor.maxL * 100)) / 100
            s = random.randint(25, 75) / 100

            r, g, b = Color.hls_to_rgb(h, l, s)

            self.generations[0].append(Square((r, g, b), (h, s, l), selectedKey, self.size / 2, self._colors))

        self.calculateColorPercentages()

    def calculateColorPercentages(self):
        total = 0
        for key, color in self._colors.items():
            total += color.squareCount

        for key, color in self._colors.items():
            color.geneticPercentage = color.squareCount / total

    def getLastGeneration(self):
        return self.generations[-1:][0]

    def getColorDistribution(self):
        return self._colors

    def nextGeneration(self):
        self.generations.append([])

    def addToLastGeneration(self, square):
        self.generations[len(self.generations) - 1].append(square)
        
