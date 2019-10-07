from probabilista import Probabilista
from imagen import Imagen

imagen = Imagen("imgs/imagen.jpg")
probabilista = Probabilista(imagen, 20, 20)

imagen.drawImagenConSalida(probabilista.elegirSamples())