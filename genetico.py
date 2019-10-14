from htmloutput import HtmlOutput
from multiprocessing import set_start_method, freeze_support, Pool
import random
class Genetico:

    def __init__(self, sectors):
        self.sectors = sectors
        self.cantGeneraciones = 0
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

        for squareWithFitness in squaresWithFitness:
            if squareWithFitness[1] >= average:
                elegibles.append(squareWithFitness)

        if len(elegibles) < 2:
            raise AssertionError("No suitable parents found")

        elegibles.sort(key=lambda squareWithFitness: squareWithFitness[1])

        sectorArea = sector.maxX - sector.minX
        newArea = 0

        for _ in range(0, int(len(elegibles) / 2)):

            firstParent = elegibles[0]
            elegibles.pop(0)

            randomIndex = random.randint(0, len(elegibles) - 1)
            randomParent = elegibles[randomIndex]
            elegibles.pop(randomIndex)


            childrenCount = random.randint(2, 6 if newArea < sectorArea * 1.5 else 2)

            for childrenIndex in range(0, childrenCount):
                child = firstParent[0].reproduceWith(randomParent[0])

                if random.randint(1, 100) < 5:
                    child.mutate()

                child.setColorDistribution(sector.getColorDistribution())

                sector.addToLastGeneration(child)
                newArea += child.size
        

    def run(self):
        for generationIndex in range(0, 101):

            self.htmlOutput.newGeneration()

            # pool = Pool()
            # pool.map(self.calculateGeneration, (sector for sector in self.sectors))
            # pool.close()

            for sector in self.sectors:
                self.calculateGeneration(sector)

            if generationIndex % 10 == 0:
                for sector in self.sectors:
                    self.htmlOutput.addInGeneration(sector.getLastGeneration(), sector)

            self.cantGeneraciones += 1
            self.htmlOutput.endGeneration()


        self.htmlOutput.write()