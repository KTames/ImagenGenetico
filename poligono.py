class Poligono:
    @staticmethod
    def codificarAdn(x1, y1, x2, y2, x3, y3, x4, y4, red, green, blue):
        # Distribución de bits:

        # Ya que el máximo de X y Y es 1023, se van a utilizar 10 bits para representar cada coordenada
        # Además sabemos que el valor máximo de red, green y blue es 255, así que se usarán 8 bits para cada color

        # Así, se da la siguiente distribución:
        # (0 - 9) -> x1
        # (10 - 19) -> y1
        # (20 - 29) -> x2
        # (30 - 39) -> y2
        # (40 - 49) -> x3
        # (50 - 59) -> y3
        # (60 - 69) -> x4
        # (70 - 79) -> y4
        # (80 - 87) -> red
        # (88 - 95) -> green
        # (96 - 103) -> blue

        # En total para cada poligono se necesitan 104 bits

        adn = 1
        adn <<= 10
        adn |= x1
        adn <<= 10
        adn |= y1

        adn <<= 10
        adn |= x2
        adn <<= 10
        adn |= y2

        adn <<= 10
        adn |= x3
        adn <<= 10
        adn |= y3

        adn <<= 10
        adn |= x4
        adn <<= 10
        adn |= y4

        adn <<= 8
        adn |= red

        adn <<= 8
        adn |= green

        adn <<= 8
        adn |= blue
        
        return adn
        
    @staticmethod
    def decodificarAdn(adn):
        x1, y1, x2, y2, x3, y3, x4, y4, red, green, blue = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

        blue = adn & 255
        adn >>= 8

        green = adn & 255
        adn >>= 8

        red = adn & 255
        adn >>= 8

        y4 = adn & 1023
        adn >>= 10
        x4 = adn & 1023
        adn >>= 10

        y3 = adn & 1023
        adn >>= 10
        x3 = adn & 1023
        adn >>= 10

        y2 = adn & 1023
        adn >>= 10
        x2 = adn & 1023
        adn >>= 10

        y1 = adn & 1023
        adn >>= 10
        x1 = adn & 1023
        adn >>= 10

        return x1, y1, x2, y2, x3, y3, x4, y4, red, green, blue