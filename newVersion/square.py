#!encoding=utf-8
from color import Color
import random


class Square:

    def __init__(self, genes):
        self.genes = genes

    def mutate(self):
        pivot = 2 ** random.randint(0, 15)

        if self.genes & pivot == 0:
            self.genes |= pivot
        else:
            self.genes &= 2 ** 16 - 1 - pivot

    def reproduce_with(self, another_parent):
        pivot = 2 ** random.randint(3, 12)

        new_genes = (pivot - 1) & self.genes
        new_genes |= ((2 ** 16 - 1) - (pivot - 1)) & another_parent.genes

        return Square(new_genes)
