#!encoding=utf-8
from PIL import Image, ImageDraw, ImageColor


class ImageData:

    def __init__(self, path):
        self._IMAGE = Image.open(path)
        self.height = self._IMAGE.height
        self.width = self._IMAGE.width

        mut = iter(self._IMAGE.getdata())
        self._draw = ImageDraw.Draw(self._IMAGE)

        # Carga una matriz de 1024x1024 con los pixeles RGB de la imagen
        self._matrix = [[() for y in range(0, self._IMAGE.height)] for x in range(0, self._IMAGE.width)]

        for coordY in range(0, self._IMAGE.height):
            for coordX in range(0, self._IMAGE.width):
                self._matrix[coordX][coordY] = mut.__next__()

    def get_point(self, x, y):
        return self._matrix[x][y]
