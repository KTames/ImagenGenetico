from probabilistic import Probabilistic
from image import ImageData
from genetic import Genetic

rows = 40
columns = 40

image = ImageData("imgs/guacamaya.jpg")
probabilistic = Probabilistic(image, rows, columns)
sectors = probabilistic.chooseSamples()

genetic = Genetic(sectors)
genetic.run()
