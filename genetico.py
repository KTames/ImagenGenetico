from htmloutput import HtmlOutput
from multiprocessing import set_start_method, freeze_support, Pool, Queue, Process
import random

print_delay = 2

class Genetico:

    def __init__(self, sectors):
        self.sectors = sectors
        self.htmlOutput = HtmlOutput()

    def calculateGeneration(self, sector): #queue
        lastGeneration = sector.getLastGeneration()

        sector.nextGeneration()

        squaresWithFitness = []
        average = 0
        length = len(lastGeneration)

        for square in lastGeneration:
            fitness = sector.getFitness(square)
            squaresWithFitness.append([square, fitness])
            average += fitness / length

        elegibles = []
        squaresToErase = []

        for index in range(0, len(squaresWithFitness)):
            squareWithFitness = squaresWithFitness[index]
            if squareWithFitness[1] >= average:
                squaresToErase.append(index)
                elegibles.append(squareWithFitness)
                # sector.addToLastGeneration(squareWithFitness[0])

        if len(elegibles) < 2:
            for index in range(len(squaresToErase) - 1, -1, -1):
                squaresWithFitness.pop(squaresToErase[index])

            squaresWithFitness.sort(
                key=lambda squareWithFitness: squareWithFitness[1])

            while len(elegibles) < 2:
                if len(squaresWithFitness) < 1:
                    raise AssertionError("No suitable parents found")
                elegibles.append(squaresWithFitness[0])
                squaresWithFitness.pop(0)
        
        childrenSize = colorDict
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

            childrenCount = random.randint(4, 8) if newArea < sectorArea * 2.5 else 2

            for childrenIndex in range(0, childrenCount):
                child = firstParent[0].reproduceWith(randomParent[0])

                if random.randint(1, 100) < 5:
                    child.mutate()

                child.setColorDistribution(sector.getColorDistribution())

                sector.addToLastGeneration(child)
                newArea += child.size
        sector.calculateColorPercentages()
        # queue.put(sector)
        return sector

    def run(self):  
        q = Queue()

        for generationIndex in range(0, 10):

            if generationIndex % print_delay == 0:
                self.htmlOutput.newGeneration()

            # tasks = []
            # for sector in self.sectors:
            #     p = Process(target=self.calculateGeneration, args=(sector, q))
            #     tasks.append(p)
            #     p.start()

            # for task in tasks:
            #     task.join()

            

            # pool = Pool()
            # pool.map(self.calculateGeneration, ((sector, q) for sector in self.sectors))
            # pool.terminate()

            # self.sectors = []
            # while not q.empty():
            #     self.sectors.append(q.get())

            for sector in self.sectors:
                self.calculateGeneration(sector)

            if generationIndex % print_delay == 0:
                for sector in self.sectors:
                    self.htmlOutput.addInGeneration(
                        sector.getLastGeneration(), sector)
                self.htmlOutput.endGeneration()

        self.htmlOutput.write()