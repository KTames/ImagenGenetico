from htmloutput import HtmlOutput
from multiprocessing import set_start_method, freeze_support, Pool
import random
class Genetico:

    def __init__(self, sectors):
        self.sectors = sectors
        self.htmlOutput = HtmlOutput()

    def calculateGeneration(self, sector):
        lastGeneration = sector.getLastGeneration()

        sector.nextGeneration()

        squaresWithFitness = []
        average = 0
        length = len(lastGeneration)

        for square in lastGeneration:
            fitness = square.getFitness()
            squaresWithFitness.append([square, fitness])
            average += fitness / length

        elegibles = []
        squaresToErase = []
        for index in range(0, len(squaresWithFitness)):
            squareWithFitness = squaresWithFitness[index]
            if squareWithFitness[1] >= average:
                squaresToErase.append(index)
                elegibles.append(squareWithFitness)

        if len(elegibles) < 2:
            for index in range(len(squaresToErase) - 1, -1, -1):
                squaresWithFitness.pop(squaresToErase[index])

            if len(squaresWithFitness) < 1:
                raise AssertionError("No suitable parents found")

            squaresWithFitness.sort(key=lambda squareWithFitness: squareWithFitness[1])

            elegibles.append(squaresWithFitness[0])
            print ("Casi se cae esta mierda jaja. Nuevo len:", len(elegibles))

        for key, color in sector.getColorDistribution().items():
                color.resetSquareCount()

        elegibles.sort(key=lambda squareWithFitness: squareWithFitness[1])

        sectorArea = sector.maxX - sector.minX
        newArea = 0

        for _ in range(0, int(len(elegibles) / 2)):

            firstParent = elegibles[0]
            elegibles.pop(0)

            randomIndex = random.randint(0, len(elegibles) - 1)
            randomParent = elegibles[randomIndex]
            elegibles.pop(randomIndex)


            childrenCount = random.randint(2, 6 if newArea < sectorArea * 5 else 2)

            for childrenIndex in range(0, childrenCount):
                child = firstParent[0].reproduceWith(randomParent[0])

                if random.randint(1, 100) < 5:
                    child.mutate()

                child.setColorDistribution(sector.getColorDistribution())

                sector.addToLastGeneration(child)
                newArea += child.size
        sector.calculateColorPercentages()
        

    def run(self):
        for generationIndex in range(0, 10):

            if generationIndex % 1 == 0:
                self.htmlOutput.newGeneration()


            # pool = Pool()
            # pool.map(self.calculateGeneration, (sector for sector in self.sectors))
            # pool.terminate()

            for sector in self.sectors:
                self.calculateGeneration(sector)

            if generationIndex % 1 == 0:
                for sector in self.sectors:
                    self.htmlOutput.addInGeneration(sector.getLastGeneration(), sector)
                self.htmlOutput.endGeneration()

        self.htmlOutput.write()