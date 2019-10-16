#!encoding=utf-8
from color import Color
import random


class Square:

    def __init__(self, genes, size):
        self.genes = genes
        self.size = size

    def mutate(self):
        pivot = 2 ** random.randint(0, 15)

        if self.genes & pivot == 0:
            self.genes |= pivot
        else:
            self.genes &= 2 ** 16 - 1 - pivot
    
    def reproduceWith(self, anotherParent):
        pivot = 2 ** random.randint(4, 10)

        newGenes = (pivot - 1) & self.genes
        newGenes |= ((2**16 - 1) - (pivot - 1)) & anotherParent.genes

        return Square(newGenes, self.size if self.size > 2 else 2)