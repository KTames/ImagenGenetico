from htmloutput import HtmlOutput
import random
from square import Square

print_delay = 5
cant_generations_per_image = 50
mutate_probability = 5


class Genetic:

    def __init__(self, sectors, image_count):
        self._sectors = sectors
        self._html_output = HtmlOutput()
        self._image_count = image_count

    @staticmethod
    def calculate_next_generation(sector, image_index):
        last_generation = sector.get_last_generation()
        sector.next_generation()
        squares_with_fitness = []
        average = 0

        generation_length = len(last_generation)

        colors_distribution = dict()  # Va a guardar la distribución de colores y cantidad de cuadrados de un color
        # que se va a tomar en cuenta para elegir si reproducir o no el cuadrado

        color_dict = sector.get_color_distribution()

        for key, color in color_dict.items():
            colors_distribution[key] = {
                "count": 0,
                "target": sector.targets_per_image[image_index][key].probability,
                "actual": 0
            }
            color.reset_square_count()

        for square in last_generation:
            fitness, key = sector.get_fitness(square)
            squares_with_fitness.append({"square": square, "color": key, "fitness": fitness})
            average += fitness / generation_length

        children_size = sector.square_size * 0.9
        children_size = children_size if children_size > 14 else 14

        sector.square_size = children_size

        data_to_reproduce = []
        data_to_erase = []

        # Evalúa todos los cuadrados y mete aquellos que cumplen con el fitness
        for data_index in range(0, len(squares_with_fitness)):
            square_data = squares_with_fitness[data_index]

            if square_data["fitness"] <= average:
                data_to_erase.append(data_index)
                data_to_reproduce.append(square_data)
                colors_distribution[square_data["color"]]["count"] += 1

        for index in range(len(data_to_erase) - 1, -1, -1):
            squares_with_fitness.pop(data_to_erase[index])  # Borra de la lista de todos los cuadrados aquellos que sí
            # pasaron el fitness

        if len(data_to_reproduce) < 2:  # Si hay sólo un cuadrado, mete en la lista el segundo mejor fitness
            while len(data_to_reproduce) < 2:
                squares_with_fitness.sort(key=lambda square_with_fitness: square_with_fitness["fitness"])
                data_to_reproduce.append(squares_with_fitness[0])
                colors_distribution[squares_with_fitness[0]["color"]]["count"] += 1

        data_to_reproduce_length = len(data_to_reproduce)
        for key, distribution in colors_distribution.items():
            distribution["actual"] = distribution["count"] / data_to_reproduce_length

        deleted_squares = []
        someone_reproduced = False
        count = 0
        while count <= 500 or not someone_reproduced:
            count += 1
            if len(data_to_reproduce) < 2:
                for key, color in colors_distribution.items():
                    if color["count"] == 0 and color["target"] > 0:
                        original_color = sector.targets_per_image[image_index][key]
                        distance = original_color.max_bit - original_color.min_bit

                        first_parent = Square(random.randint(int(original_color.min_bit + distance / 4),
                                                             int(original_color.max_bit - distance / 4)))
                        second_parent = Square(random.randint(int(original_color.min_bit + distance / 4),
                                                              int(original_color.max_bit - distance / 4)))

                        Genetic.reproduce_parents(
                            color_dict, {"square": first_parent},
                            {"square": second_parent},
                            sector
                        )
                        someone_reproduced = True

                    if not someone_reproduced:
                        Genetic.reproduce_parents(
                            color_dict, deleted_squares[0],
                            data_to_reproduce[0],
                            sector
                        )
                break

            first_parent = Genetic.pick_random_parent(data_to_reproduce)
            color = colors_distribution[first_parent["color"]]

            if color["actual"] > color["target"]:  # Si se está por encima del target se quita y se ajustan %
                data_to_reproduce_length = Genetic.delete_square(color, colors_distribution, data_to_reproduce_length,
                                                                 deleted_squares, first_parent)
                continue

            second_parent = Genetic.pick_random_parent(data_to_reproduce)
            color = colors_distribution[second_parent["color"]]

            if color["actual"] > color["target"]:  # Si se está por encima del target se quita y se ajustan %
                data_to_reproduce.append(first_parent)
                data_to_reproduce_length = Genetic.delete_square(color, colors_distribution, data_to_reproduce_length,
                                                                 deleted_squares, second_parent)
                continue

            someone_reproduced = True
            Genetic.reproduce_parents(color_dict, first_parent, second_parent, sector)

        sector.calculate_color_percentages()

    @staticmethod
    def pick_random_parent(data_to_reproduce):
        random_index = random.randint(0, len(data_to_reproduce) - 1)
        first_parent = data_to_reproduce[random_index]
        data_to_reproduce.pop(random_index)
        return first_parent

    @staticmethod
    def reproduce_parents(color_dict, first_parent, second_parent, sector):
        for _ in range(0, 4):
            child = first_parent["square"].reproduce_with(second_parent["square"])

            if random.randint(0, 100) < mutate_probability:
                child.mutate()

            for key, color in color_dict.items():
                if color.matches_genes(child.genes):
                    color.increase_square_count()
                    break

            sector.add_to_last_generation(child)

    @staticmethod
    def delete_square(color, colors_distribution, data_to_reproduce_length, deleted_squares, first_parent):
        deleted_squares.append(first_parent)
        color["count"] -= 1
        data_to_reproduce_length -= 1
        for key, distribution in colors_distribution.items():
            distribution["actual"] = distribution["count"] / data_to_reproduce_length
        return data_to_reproduce_length

    def run(self):
        for imageIndex in range(0, self._image_count):
            for generationIndex in range(0, cant_generations_per_image):

                if generationIndex % print_delay == 0:
                    self._html_output.new_generation()

                for sector in self._sectors:
                    self.calculate_next_generation(sector, imageIndex)

                if generationIndex % print_delay == 0:
                    for sector in self._sectors:
                        self._html_output.add_in_generation(sector)

        self._html_output.write()
