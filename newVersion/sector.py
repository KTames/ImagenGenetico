#!encoding=utf-8
from color import Color, getColors
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
        self.probability = 1
        self.points = []
        self._colors = getColors()
        self.generations = [[]]
        self.size = maxX - minX
        self.squareSize = self.size / 2

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
        
        actualBitPosition = 0
        lastKey = ""
        for key, color in self._colors.items():
            if color.probability > 0:
                lastKey = key
                lowBound = actualBitPosition
                highBound = (2**16) * color.probability + lowBound
                color.setBitBounds(int(lowBound), int(highBound))
                actualBitPosition = int(highBound)
        
        self._colors[lastKey].setMaxBound(2 ** 16 - 1)
        self._createFirstGeneration()


    def _createFirstGeneration(self):
        for index in range(0, 3):
            genes = random.randint(0, 2**16 - 1)

            for key, color in self._colors.items():
                if color.matchesGenes(genes):
                    color.increaseSquareCount()
                    break

            self.generations[0].append(Square(genes, self.squareSize))
        self.calculateColorPercentages()

    def calculateColorPercentages(self):
        total = 0
        for key, color in self._colors.items():
            total += color.squareCount
        for key, color in self._colors.items():
            color.geneticPercentage = color.squareCount / total

    def getLastGeneration(self):
        return self.generations[len(self.generations) - 1]

    def getColorDistribution(self):
        return self._colors

    def nextGeneration(self):
        self.generations.append([])

    def addToLastGeneration(self, square):
        self.generations[len(self.generations) - 1].append(square)

    def getFitness(self, square):
        return True
        
