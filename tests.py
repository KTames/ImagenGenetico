#!encoding=utf-8
from multiprocessing import Process, freeze_support, set_start_method
from probabilista import Probabilista
from imagen import Imagen
from genetico import Genetico
from color import Color
import colorsys
import sys
import os

if __name__ == "__main__":
    freeze_support()
    set_start_method('spawn')
    columnas = 40
    filas = 40
    imagen = Imagen("imgs/imagen.jpg")
    probabilista = Probabilista(imagen, filas, columnas)
    sectores = probabilista.elegirSamples()

    # imagen.drawImagenConSalida(sectores)

    genetico = Genetico(sectores)
    genetico.run()