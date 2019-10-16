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
        g |= anG & 2**pivotG
        b |= anB & 2**pivotB

        hlsColor = Color.rgb_to_hls(r, g, b)
        
        selectedKey = ""
        for key, color in self.colorDistribution.items():
            if color.matches(hlsColor):
                selectedKey = key
                break
        
        return Square((r, g, b), hlsColor, selectedKey, self.size * 0.8 if self.size > 1 else self.size)
    
    def reproduceWithHLS(self, anotherParent):
        h, s, l = self.hlsColor
        anH, anS, anL = anotherParent.hlsColor

        h = int(h * 100)
        s = int(s * 100)
        l = int(l * 100)

        anH = int(anH * 100)
        anS = int(anS * 100)
        anL = int(anL * 100)


        # Se hace de 0 a 5 para dejar al menos dos bits del primer padre
        pivotH = random.randint(0,4)
        pivotS = random.randint(0,4)
        pivotL = random.randint(0,4)

        # Se dejan sólo los bits altos del primer padre
        h &= 127 - 2**(pivotH + 1) + 1
        s &= 127 - 2**(pivotS + 1) + 1
        l &= 127 - 2**(pivotL + 1) + 1

        h |= anH & 2**pivotH
        s |= anS & 2**pivotS
        l |= anL & 2**pivotL

        h = h if h <= 100 else 100
        s = s if s <= 100 else 100
        l = l if l <= 100 else 100
        h /= 100
        s /= 100
        l /= 100

        rgbColor = Color.hls_to_rgb(h, s, l)

        selectedKey = ""
        for key, color in self.colorDistribution.items():
            if color.matches((h, l, s)):
                selectedKey = key
                break
        
        return Square(rgbColor, (h, l, s), selectedKey, self.size * 0.8 if self.size > 1 else self.size)


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
        
        # previousDif = Color.getDifference(colorDict)
        previousDif = abs(colorDict[self.colorType][1] - colorDict[self.colorType][2])

        colorDict[self.colorType][0] -= self.size
        total -= self.size

        for key, color in colorDict.items():
            color[2] = color[0] / total
        # for value in values:
        #     value.append(value[0] / total)

        # newDif = Color.getDifference(colorDict)
        newDif = abs(colorDict[self.colorType][1] - colorDict[self.colorType][2])


        return newDif - previousDif

