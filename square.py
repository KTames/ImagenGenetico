#!encoding=utf-8
from color import Color, getColores
import random


class Square:

    def __init__(self, rgbColor, hlsColor, colorType, size, colorDistribution = None):
        self.rgbColor = rgbColor
        self.hlsColor = hlsColor
        self.colorType = colorType
        self.size = size
        self.colorDistribution = colorDistribution
        if colorDistribution != None:
            self.colorDistribution[colorType].increaseSquareCount(size)

    def setRGB(self, r, g, b):
        self.rgbColor = (r, g, b)
        self.hlsColor = Color.rgb_to_hls(r, g, b)

        if self.colorDistribution != None:

            self.colorDistribution[self.colorType].decreaseSquareCount(self.size)
            for key, color in self.colorDistribution:
                if color.matches(self.hlsColor):
                    self.colorType = key
                    break
            self.colorDistribution[self.colorType].increaseSquareCount(self.size)

    def setColorDistribution(self, colorDistribution):
        if self.colorDistribution != None:
            self.colorDistribution[self.colorType].decreaseSquareCount(self.size)
        self.colorDistribution = colorDistribution
        colorDistribution[self.colorType].increaseSquareCount(self.size)

    def mutate(self):
        colorIndex = random.randint(0, 2)
        bitIndex = random.randint(0, 7)

        color = int(self.rgbColor[colorIndex])

        pivot = 2**bitIndex

        if color & pivot != 0:
            inversed = 255 - pivot
            color &= inversed
        else:
            color |= pivot

        self.setRGB(
            self.rgbColor[0] if colorIndex != 0 else color,
            self.rgbColor[1] if colorIndex != 1 else color,
            self.rgbColor[2] if colorIndex != 2 else color
        )

    def reproduceWith(self, anotherParent):
        r, g, b = self.rgbColor
        r = int(r)
        g = int(g)
        b = int(b)

        # Se hace de 0 a 5 para dejar al menos dos bits del primer padre
        pivotR = random.randint(0,5)
        pivotG = random.randint(0,5)
        pivotB = random.randint(0,5)

        # Se dejan sólo los bits altos del primer padre
        r &= 255 - 2**(pivotR + 1) + 1
        g &= 255 - 2**(pivotG + 1) + 1
        b &= 255 - 2**(pivotB + 1) + 1

        anR, anB, anG = anotherParent.rgbColor
        anR = int(anR)
        anG = int(anG)
        anB = int(anB)
        r |= anR & 2**pivotR
        g |= anG & 2**pivotR
        b |= anB & 2**pivotR

        hlsColor = Color.rgb_to_hls(r, g, b)
        
        selectedKey = ""
        for key, color in self.colorDistribution.items():
            if color.matches(hlsColor):
                selectedKey = key
                break
        
        return Square((r, g, b), hlsColor, selectedKey, self.size / 2 if self.size > 4 else self.size)


    def getFitness(self):
        if self.colorDistribution == None:
            raise AttributeError("Color Distribution cannot be null")
            
        keys = []
        values = []
        total = 0

        for key, color in self.colorDistribution.items():
            keys.append(key)
            values.append([color.squareCount, color.probability])
            total += color.squareCount

        for value in values:
            value.append(value[0] / total)

        colorDict = dict(zip(keys, values))
        
        previousDif = Color.getDifference(colorDict)

        colorDict[self.colorType][0] -= self.size
        total -= self.size

        for value in values:
            value.append(value[0] / total)

        newDif = Color.getDifference(colorDict)


        return newDif - previousDif

