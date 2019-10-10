import random
import imagen
from collections import defaultdict
import colorsys
import imageio
# import matplotlib.pyplot as plt
from sector import Sector


class Probabilista:
    _imagen = None
    _filas = 0
    _columnas = 0
    _colorsRGB = defaultdict(int)
    _colorsHLS = defaultdict(int)

    def __init__(self, imagen, filas, columnas):
        self._imagen = imagen
        self._filas = filas
        self._columnas = columnas

    def _crearSectores(self):
        anchoPorSector = self._imagen.ancho / self._columnas
        altoPorSector = self._imagen.alto / self._filas

        # Calcula los X y Y de cada sector y le pone una probabilidad por defecto
        sectores = [
            Sector(
                columna,
                fila,
                int(anchoPorSector * columna),
                int(altoPorSector * fila),
                int(anchoPorSector * (columna + 1)),
                int(altoPorSector * (fila + 1))
            ) for fila in range(0, self._filas)
            for columna in range(0, self._columnas)
        ]

        return sectores

    def _elegirSector(self, sectores, indiceProbabilistico):
        indiceSector = -1
        length = len(sectores)
        while indiceProbabilistico >= 0 and indiceSector + 1 < length:
            indiceSector += 1
            indiceProbabilistico -= sectores[indiceSector].probabilidad
        return indiceSector

    def elegirSamples(self):
        # Se va a tomar un 7% de los puntos como sample
        cantSamples = int(self._imagen.alto * self._imagen.ancho * 0.05)
        # Aloja la sumatoria de las probabilidades de cada sector
        cantElementosProbabilidad = self._filas * self._columnas
        sectores = self._crearSectores()

        for count in range(0, cantSamples):
            # Elige un sector, es aquí donde entra la probabilidad
            indiceAleatorio = random.random() * cantElementosProbabilidad
            indiceSector = self._elegirSector(sectores, indiceAleatorio)
            sectorElegido = sectores[indiceSector]

            coordXrandom = random.randint(
                sectorElegido.minX, sectorElegido.maxX - 1)
            coordYrandom = random.randint(
                sectorElegido.minY, sectorElegido.maxY - 1)

            point = self._imagen.getPunto(coordXrandom, coordYrandom)

            # self._imagen.dibujarPunto((coordXrandom, coordYrandom), (0, 255, 0))
            if not (point[0] > 230 and point[1] > 230 and point[2] > 230):
                self._imagen.dibujarPunto(
                    (coordXrandom, coordYrandom), (0, 255, 0))
                if sectores[indiceSector].probabilidad < 100:
                    sectores[indiceSector].probabilidad += 0.05
                    cantElementosProbabilidad += 0.05
                # endif
                sectores[indiceSector].points.append(point)

        for sector in sectores:
            sector.calculateColors()
        return sectores

    # def getColores(self, pixeles):
    #     self.pixeles = elegirSamples.puntosElegidos
    #     pix = pixeles.getdata()

    #     for pixel in pixeles:
    #         _colorsRGB[pixel] += 1

    #     return _colorsRGB

    # def convertRGBinHSL(self, colors, nColors):
    #     self.colors = getColores(self, pixeles)
    #     self.nColors = _colorsHLS

    #     for val in colors.items():
    #         c = colorsys.rgb_to_hls(val)
    #         if c < 25.0 or c[0] > 335.0 and c[0] < 360.0:
    #             nColors["Rojo"] = c
    #         elif c[0] < 50.0:
    #             nColors["Naranja"] = c
    #         elif c[0] < 65.0:
    #             nColors["Amarillo"] = c
    #         elif c[0] < 160.0:
    #             nColors["Verde"] = c
    #         elif c[0] < 190.0:
    #             nColors["Celeste"] = c
    #         elif c[0] < 265.0:
    #             nColors["Azul"] = c
    #         elif c[0] < 285.0:
    #             nColors["Morado"] = c
    #         elif c[0] < 335.0:
    #             nColors["Rosado"] = c
    #         elif c[1] < 11.0:
    #             nColors["Negro"] = c
    #         elif c[1] > 95:
    #             nColors["Blanco"] = c

    #     return nColors
