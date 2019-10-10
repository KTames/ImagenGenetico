from probabilista import Probabilista
from imagen import Imagen
from genetico import Genetico
import colorsys
# import svgwrite

imagen = Imagen("imgs/imagen.jpg")
probabilista = Probabilista(imagen, 20, 20)
sectores = probabilista.elegirSamples()
print("Samples loaded")
imagen.drawImagenConSalida(sectores)
print("Image loaded")

index = 0
for x in range(0, 20):
    for y in range(0, 20):
        i = sectores[i]
        print(str("").center(40, '#'))
        for k, c in i.getColors().items():
            if (c.probability > 0):
                print(k.center(20), c.probability)
# print(colorsys.rgb_to_hls(93, 28, 22))

# sectores = probabilista.elegirSamples()
# genetico = Genetico();