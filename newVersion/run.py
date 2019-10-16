from probabilistic import Probabilistic
from image import ImageData
from genetic import Genetic

if __name__ == "__main__":
    rows = 4
    columns = 4

    images = [ImageData("imgs/guacamaya.jpg"), ImageData("imgs/Beach.jpg"), ImageData("imgs/imagen.jpg")]
    probabilistic = Probabilistic(images, rows, columns)
    sectors = probabilistic.chooseSamples()

    genetic = Genetic(sectors, len(images))
    genetic.run()