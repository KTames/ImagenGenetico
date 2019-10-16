from probabilistic import Probabilistic
from image import ImageData
from genetic import Genetic

rows = 4
columns = 4

image = ImageData("imgs/guacamaya.jpg")
image2 = ImageData("imgs/Beach.jpg")
image3 = ImageData("imgs/imagen.jpg")

probabilistic = Probabilistic([image, image2, image3], rows, columns)
sectors = probabilistic.chooseSamples()

genetic = Genetic(sectors)
genetic.run()
