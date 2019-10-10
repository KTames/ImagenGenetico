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
for y in range(0, 20):
    for x in range(0, 20):
        i = sectores[index]
        index += 1
        strings = []
        for k, c in i.getColors().items():
            if (c.probability > 0):
                strings.append(k.center(20) + str(c.probability))

        if not(len(strings) == 1 and "white" in strings[0]):
            print(str(" " + str(x) + ", " + str(y) + " ").center(40, '#'))
            for s in strings:
                print(s)
            print("\n")
# print(colorsys.rgb_to_hls(93, 28, 22))

# sectores = probabilista.elegirSamples()
# genetico = Genetico();