#!encoding=utf-8
import random
from sector import Sector


class Probabilistic:

    def __init__(self, images, rows, columns):
        self._images = images
        self._rows = rows
        self._columns = columns

    def _create_sectors(self):

        width_per_sector = self._images[0].width / self._columns
        height_per_sector = self._images[0].height / self._rows

        # Calcula los X y Y de cada sector
        sectors = [
            Sector(
                column,
                row,
                int(width_per_sector * column),
                int(height_per_sector * row),
                int(width_per_sector * (column + 1)),
                int(height_per_sector * (row + 1))
            ) for row in range(0, self._rows)
            for column in range(0, self._columns)
        ]

        return sectors

    @staticmethod
    def _choose_sector(sectors, probabilistic_index):
        index_sector = -1
        length = len(sectors)
        while probabilistic_index >= 0 and index_sector + 1 < length:
            index_sector += 1
            probabilistic_index -= sectors[index_sector].probability
        return index_sector

    def choose_samples(self):
        image_index = 0
        sectors = self._create_sectors()
        cant_probability_elements = self._rows * self._columns * 10

        for image in self._images:

            for sector in sectors:
                sector.points.append([])

            # Se va a tomar un 7% de los puntos como sample
            cant_samples = int(image.height * image.width * 0.07)

            # Aloja la sumatoria de las probabilidades de cada sector
            for count in range(0, cant_samples):

                # Elige un sector, es aquí donde entra la probabilidad
                random_index = random.random() * cant_probability_elements
                sector_index = self._choose_sector(sectors, random_index)
                choosen_sector = sectors[sector_index]

                coord_x_random = random.randint(
                    choosen_sector.min_x, choosen_sector.max_x - 1)
                coord_y_random = random.randint(
                    choosen_sector.min_y, choosen_sector.max_y - 1)

                point = image.get_point(coord_x_random, coord_y_random)

                if not (point[0] > 230 and point[1] > 230 and point[2] > 230):  # Si el punto no es blanco
                    if sectors[sector_index].probability < 100:

                        sectors[sector_index].probability += 0.05
                        cant_probability_elements += 0.05

                    elif sectors[sector_index].probability > 2:  # Si el punto sí es blanco

                        sectors[sector_index].probability -= 0.05
                        cant_probability_elements -= 0.05

                sectors[sector_index].points[image_index].append(point)
            image_index += 1

        for sector in sectors:
            sector.calculate_colors()

        return sectors
