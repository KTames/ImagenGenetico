#!encoding=utf-8
from PIL import Image, ImageDraw, ImageColor

class Imagen:
    # _IMAGEN = Image.new()
    # _draw = ImageDraw.Draw()
    # _matriz = []
    # alto = 0
    # ancho = 0

    def __init__(self, path):
        self._IMAGEN = Image.open(path)
        self.alto = self._IMAGEN.height
        self.ancho = self._IMAGEN.width

        mut = iter(self._IMAGEN.getdata())
        self._draw = ImageDraw.Draw(self._IMAGEN)

        # Carga una matriz de 1024x1024 con los pixeles RGB de la imagen
        self._matriz = [[() for y in range(0, self._IMAGEN.height)] for x in range(0, self._IMAGEN.width)]

        for coordenadaY in range(0, self._IMAGEN.height):
            for coordenadaX in range(0, self._IMAGEN.width):
                self._matriz[coordenadaX][coordenadaY] = mut.__next__()


    def drawImagenConSalida(self, salida):
        for s in salida:
            if s.probabilidad <= 1 and False:
                self._draw.rectangle((
                    s.minX, s.minY,
                    s.maxX, s.maxY,
                ),0)
            else:
                self._draw.line((
                    s.minX, s.minY,
                    s.minX, s.maxY,
                    s.maxX, s.maxY,
                    s.maxX, s.minY,
                    s.minX, s.minY
                    ), 0)
        self._IMAGEN.show()

    def getPunto(self, x, y):
        return self._matriz[x][y]

    def dibujarPunto(self, xy, fill):
        self._draw.point(xy, fill)