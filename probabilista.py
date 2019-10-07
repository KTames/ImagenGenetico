import random
import imagen

class Probabilista:
    _imagen = None
    _filas = 0
    _columnas = 0

    def __init__(self, imagen, filas, columnas):
        self._imagen = imagen
        self._filas = filas
        self._columnas = columnas

    def _crearSectores(self):    
        anchoPorSector = self._imagen.ancho / self._columnas
        altoPorSector = self._imagen.alto / self._filas

        # Calcula los X y Y de cada sector y le pone una probabilidad por defecto 
        sectores = [
            {
                'logicX': columna,
                'logicY': fila,
                'minX': int(anchoPorSector * columna),
                'minY': int(altoPorSector * fila),
                'maxX': int(anchoPorSector * (columna + 1)),
                'maxY': int(altoPorSector * (fila + 1)),
                'cantidadPuntos': 0,
                'puntos': [],
                'probabilidad': 1
            } for fila in range(0, self._filas)
            for columna in range(0, self._columnas)
        ]

        return sectores

    def _elegirSector(self, sectores, indiceProbabilistico):
        indiceSector = -1
        length = len(sectores)
        while indiceProbabilistico >= 0 and indiceSector + 1 < length:
            indiceSector += 1
            indiceProbabilistico -= sectores[indiceSector]['probabilidad']
        return indiceSector

    

    def elegirSamples(self):
        cantSamples = int(self._imagen.alto * self._imagen.ancho * 0.07) # Se va a tomar un 7% de los puntos como sample
        cantElementosProbabilidad = self._filas * self._columnas # Aloja la sumatoria de las probabilidades de cada sector
        sectores = self._crearSectores()
        puntosElegidos = []

        for count in range(0, cantSamples):
            indiceAleatorio = random.random() * cantElementosProbabilidad # Elige un sector, es aquí donde entra la probabilidad
            indiceSector = self._elegirSector(sectores, indiceAleatorio)
            sectorElegido = sectores[indiceSector]

            coordXrandom = random.randint(sectorElegido['minX'], sectorElegido['maxX'] - 1)
            coordYrandom = random.randint(sectorElegido['minY'], sectorElegido['maxY'] - 1)

            punto = self._imagen.getPunto(coordXrandom,coordYrandom)

            # self._imagen.dibujarPunto((coordXrandom, coordYrandom), (0, 255, 0))
            if not (punto[0] > 230 and punto[1] > 230 and punto[2] > 230):
                self._imagen.dibujarPunto((coordXrandom, coordYrandom), (0, 255, 0))
                if sectores[indiceSector]['probabilidad'] < 100:
                    sectores[indiceSector]['probabilidad'] += 0.05
                    cantElementosProbabilidad += 0.05
                # endif
                sectores[indiceSector]['cantidadPuntos'] += 1
                sectores[indiceSector]['puntos'].append(punto)
                puntosElegidos.append(punto)

        return [sectores, puntosElegidos]
    
    @staticmethod
    def generarPoblacionInicial(salida):
        pass