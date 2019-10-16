from htmloutput import HtmlOutput
import random

print_delay = 2
cant_generations = 10
mutate_probability = 5

class Genetic:

    def __init__(self, sectors, imageCount):
        self._sectors = sectors
        self._htmlOutput = HtmlOutput()
        self._imageCount = imageCount

    def calculateNextGeneration(self, sector):
        lastGeneration = sector.getLastGeneration()

        sector.nextGeneration()

        squaresWithFitness = []
        average = 0
        length = len(lastGeneration)

        for square in lastGeneration:
            fitness = sector.getFitness(square)
            squaresWithFitness.append([square, fitness])
            average += fitness / length
        
        colorDict = sector.getColorDistribution()
        
        childrenSize = sector.squareSize * 0.9
        childrenSize = childrenSize if childrenSize > 2 else 2
        sector.squareSize = childrenSize

        for key, color in colorDict.items():
            color.resetSquareCount()
        
        for _ in range(0, int(len(squaresWithFitness) / 2)):
            firstParent = squaresWithFitness[0]
            squaresWithFitness.pop(0)
            
            randomIndex = random.randint(0, len(squaresWithFitness) - 1)
            randomParent = squaresWithFitness[randomIndex]
            squaresWithFitness.pop(randomIndex)

            for _ in range(0, 3):
                child = firstParent.reproduceWith(randomParent)
                
                if random.randint(0, 100) < mutate_probability:
                    child.mutate()

                for key, color in colorDict.items():
                    if color.matchesGenes(child.genes):
                        color.increaseSquareCount()
                        break

                sector.addToLastGeneration(child)
        
        sector.calculateColorPercentages()
            

    def run(self):
        for generationIndex in range(0, cant_generations):
            
            if generationIndex % print_delay == 0:
                self._htmlOutput.newGeneration()
            
            for sector in self._sectors:
                self.calculateNextGeneration(sector)

            if generationIndex % print_delay == 0:
                for sector in self._sectors:
                    self._htmlOutput.addInGeneration(sector)
        
        self._htmlOutput.write()
