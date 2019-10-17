#!encoding=utf-8
from color import Color, get_colors
import random
from square import Square


class Sector:

    def __init__(self, logic_x, logic_y, min_x, min_y, max_x, max_y):
        self.logic_x = logic_x
        self.logic_y = logic_y
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.probability = 10
        self.points = []
        self._colors = get_colors()
        self.generations = [[]]
        self.size = max_x - min_x
        self.square_size = self.size / 2
        self.targets_per_image = []

    def get_colors(self):
        return self._colors

    def calculate_colors(self):
        """
            Calcula los porcentajes de color de los puntos que se eligieron en el probabilista
        """

        colors_temp = [get_colors() for _ in range(0, len(self.points))]

        for imageIndex in range(0, len(self.points)):

            count_points = len(self.points[imageIndex])

            if count_points == 0:
                self._colors["white"].set_probability(1)

            else:
                cant_colors = 0
                points_to_evaluate = int(
                    count_points * (1. / 3.)
                ) if count_points > 500 else count_points

                points_to_evaluate = points_to_evaluate if points_to_evaluate < 500 else 500

                for pointIndex in range(0, points_to_evaluate):
                    rand = random.randint(0, count_points - 1)

                    point = self.points[imageIndex][rand]
                    hls = Color.rgb_to_hls(point[0], point[1], point[2])

                    for key, color in colors_temp[imageIndex].items():
                        if color.matches(hls):
                            cant_colors += 1
                            color.increment_count()
                            break

                for key, color in colors_temp[imageIndex].items():
                    color.set_probability(color.cant_points / cant_colors)

                self.targets_per_image = colors_temp

        actual_bit_position = 0
        last_key = ""
        image_count = len(colors_temp)

        for key, color in self._colors.items():
            total_sum = 0
            for index in range(0, image_count):
                total_sum += colors_temp[index][key].probability

            if total_sum > 0:
                last_key = key
                low_bound = actual_bit_position
                high_bound = (2 ** 16) * (total_sum / image_count) + low_bound
                color.set_bit_bounds(int(low_bound), int(high_bound))
                actual_bit_position = int(high_bound)

        self._colors[last_key].set_max_bound(2 ** 16 - 1)
        self._create_first_generation()

    def _create_first_generation(self):
        for index in range(0, 3):
            genes = random.randint(0, 2 ** 16 - 1)

            for key, color in self._colors.items():
                if color.matches_genes(genes):
                    color.increase_square_count()
                    break

            self.generations[0].append(Square(genes))
        self.calculate_color_percentages()

    def calculate_color_percentages(self):
        total = 0
        for key, color in self._colors.items():
            total += color.square_count
        for key, color in self._colors.items():
            color.genetic_percentage = color.square_count / total

    def get_last_generation(self):
        return self.generations[len(self.generations) - 1]

    def get_color_distribution(self):
        return self._colors

    def next_generation(self):
        self.generations.append([])

    def add_to_last_generation(self, square):
        self.generations[len(self.generations) - 1].append(square)

    def get_fitness(self, square):
        genes = square.genes
        target = 0
        color_key = ""
        for key, color in self._colors.items():
            if color.matches_genes(genes):
                target = color.target
                color_key = key
                break

        return (abs(genes - target) / target), color_key
