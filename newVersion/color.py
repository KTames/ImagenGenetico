#!encoding=utf-8
import colorsys


class Color:

    @staticmethod
    def rgb_to_hls(r, g, b):
        r, g, b = [x / 255.0 for x in [r, g, b]]
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        return h, l, s

    @staticmethod
    def hls_to_rgb(h, l, s):
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return r * 255, g * 255, b * 255

    def __init__(self, min_h, max_h, min_l, max_l, rgb_color):
        self.rgb_color = rgb_color
        self.min_h = min_h
        self.max_h = max_h
        self.min_l = min_l
        self.max_l = max_l
        self.cant_points = 0
        self.probability = 0
        self.square_count = 0
        self.genetic_percentage = 0
        self.min_bit = -1
        self.max_bit = -1
        self.target = 0

    def matches(self, hls_color):
        return self.min_h <= hls_color[0] <= self.max_h and hls_color[1] >= self.min_l and hls_color[
            1] <= self.max_l

    def increment_count(self):
        self.cant_points += 1

    def set_probability(self, prob):
        self.probability = prob

    def set_bit_bounds(self, minimum, maximum):
        self.min_bit = minimum
        self.target = int(minimum + maximum / 2)
        self.max_bit = maximum

    def set_max_bound(self, maximum):
        self.max_bit = maximum
        self.target = int(self.min_bit + maximum / 2)

    def matches_genes(self, genes):
        return self.max_bit >= genes >= self.min_bit

    def increase_square_count(self):
        self.square_count += 1

    def decrease_square_count(self):
        self.square_count -= 1

    def reset_square_count(self):
        self.square_count = 0
        self.genetic_percentage = 0


def get_colors():
    return {
        "black": Color(0, 1, 0, 0.11, (0, 0, 0)),
        "white": Color(0, 1, 0.97, 1, (255, 255, 255)),

        "red": Color(0, 0.07, 0.5, 1, (242, 13, 13)),
        "darkred": Color(0, 0.07, 0, 0.5, (97, 5, 5)),

        "orange": Color(0.07, 0.14, 0.5, 1, (244, 119, 42)),
        "darkorange": Color(0.07, 0.14, 0, 0.5, (111, 46, 6)),

        "yellow": Color(0.14, 0.18, 0.5, 1, (242, 215, 13)),
        "darkyellow": Color(0.14, 0.18, 0, 0.5, (121, 108, 6)),

        "green": Color(0.18, 0.44, 0.5, 1, (81, 255, 0)),
        "darkgreen": Color(0.18, 0.44, 0, 0.5, (37, 117, 0)),

        "cyan": Color(0.44, 0.53, 0.5, 1, (0, 255, 242)),
        "darkcyan": Color(0.44, 0.53, 0, 0.5, (0, 128, 121)),

        "blue": Color(0.53, 0.74, 0.5, 1, (5, 5, 255)),
        "darkblue": Color(0.53, 0.74, 0, 0.5, (0, 2, 128)),

        "purple": Color(0.74, 0.79, 0.5, 1, (94, 47, 202)),
        "darkpurple": Color(0.74, 0.79, 0, 0.5, (48, 24, 103)),

        "pink": Color(0.79, 0.93, 0.5, 1, (236, 0, 240)),
        "darkpink": Color(0.79, 0.93, 0, 0.5, (100, 0, 102)),

        "red2": Color(0.93, 1, 0, 1, (242, 13, 13)),
        "darkred2": Color(0.93, 1, 0, 1, (97, 5, 5)),
    }
