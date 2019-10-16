#!encoding=utf-8
import random
from collections import defaultdict
import colorsys
from multiprocessing import Pool
from sector import Sector


class Probabilistic:

    def __init__(self, images, rows, columns):
        self._images = images
        self._rows = rows
        self._columns = columns

    def _createSectors(self):
        widthPerSector = self._images[0].width / self._columns
        heightPerSector = self._images[0].height / self._rows

        # Calcula los X y Y de cada sector y le pone una probabilidad por defecto
        sectors = [
            Sector(
                column,
                row,
                int(widthPerSector * column),
                int(heightPerSector * row),
                int(widthPerSector * (column + 1)),
                int(heightPerSector * (row + 1))
            ) for row in range(0, self._rows)
            for column in range(0, self._columns)
        ]

        return sectors

    def _chooseSector(self, sectors, probabilisticIndex):
        indexSector = -1
        length = len(sectors)
        while probabilisticIndex >= 0 and indexSector + 1 < length:
            indexSector += 1
            probabilisticIndex -= sectors[indexSector].probability
        return indexSector

    def chooseSamples(self):
        imageIndex = 0
        sectors = self._createSectors()
        cantProbabilityElements = self._rows * self._columns * 10

        for image in self._images:

            for sector in sectors:
                sector.points.append([])
            # Se va a tomar un 7% de los puntos como sample
            cantSamples = int(image.height * image.width * 0.05)
            # Aloja la sumatoria de las probabilidades de cada sector
            for count in range(0, cantSamples):
                # Elige un sector, es aquí donde entra la probabilidad
                randomIndex = random.random() * cantProbabilityElements
                sectorIndex = self._chooseSector(sectors, randomIndex)
                choosenSector = sectors[sectorIndex]

                coordXrandom = random.randint(
                    choosenSector.minX, choosenSector.maxX - 1)
                coordYrandom = random.randint(
                    choosenSector.minY, choosenSector.maxY - 1)

                point = image.getPoint(coordXrandom, coordYrandom)

                # self._imagen.dibujarPunto((coordXrandom, coordYrandom), (0, 255, 0))
                if not (point[0] > 230 and point[1] > 230 and point[2] > 230):
                    if sectors[sectorIndex].probability < 100:

                        sectors[sectorIndex].probability += 0.05
                        cantProbabilityElements += 0.05
                        
                    elif sectors[sectorIndex].probability > 2:

                        sectors[sectorIndex].probability -= 0.05
                        cantProbabilityElements -= 0.05

                sectors[sectorIndex].points[imageIndex].append(point)
            imageIndex += 1
            
        for sector in sectors:
            sector.calculateColors()

        return sectors