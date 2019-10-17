import random


class HtmlOutput:

    def __init__(self):
        self.output = [
            '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" '
            'content="width=device-width, initial-scale=1.0"><meta http-equiv="X-UA-Compatible" '
            'content="ie=edge"><title>Output</title><style>* {padding: 0;margin: 0;font-family: Arial, Helvetica, '
            'sans-serif}body {background-color: #111;}input[type=number] {padding: 5px;width: 300px;font-size: '
            '15px;color: whitesmoke;background-color: #353535;}#container {display: block;border: 1px solid '
            'black;width: 100vw;height: 400px;padding: 0 1rem;overflow: hidden;background-color: #fafafa;}svg {width: '
            '400px;height: 400px;margin: auto;}table {width: 1200px;border-collapse: collapse;margin: 20px calc(50vw '
            '- 600px);}td {padding: 1rem;width: 50%;}td:first-child {text-align: right;color: white;}button {width: '
            '100%;border-radius: 20px;border: 0;box-shadow: 0 0 5px;padding: 10px;user-select: '
            'none;}</style></head><body><div><table><tr><td><label for="iNumber">Tiempo de animación ('
            'segundos)</label></td><td><input type="number" name="iNumber" id="iNumber" '
            'value="20.0"></td></tr><tr><td colspan="2"><button id="btn">Play</button></td></tr></table></div><div '
            'id="container"><svg id="svg" viewBox="0 0 1024 1024"style="transition-property: '
            'all;transition-timing-function: linear;margin-left: 0;"></svg></div><script>const svg = '
            'document.getElementById("svg");const container = document.getElementById("container");const button = '
            'document.getElementById("btn");const durationBox = document.getElementById("iNumber");button.onclick = '
            'restart;const shapes = [',
            [],
            '];let duration = parseFloat(durationBox.value) * 1000;let stepSleep = 0;function restart() {duration = '
            'parseFloat(durationBox.value) * 1000;stepSleep = duration / shapes.length;button.innerHTML = '
            '"Replay";svg.style.transitionDuration = "0s";svg.style.marginLeft = "0";setTimeout(play, 100);}function '
            'play() {svg.style.transitionDuration = duration + "ms";setTimeout(function(){svg.style.marginLeft = ('
            'container.clientWidth - svg.clientWidth) + "px";animate();}, 100);}function animate(index = 0) {if ('
            'index < shapes.length) {svg.innerHTML = shapes[index];setTimeout(function() {animate(index + 1)}, '
            'stepSleep);}}</script></body></html> '
        ]
        self.count = 0

    def new_generation(self):
        self.output[1].append("")

    def add_in_generation(self, sector):
        output = ""
        sector_size = sector.max_x - sector.min_x
        color_distribution = sector.get_colors()
        size = sector.square_size

        for key, color in color_distribution.items():
            r, g, b = color.rgb_color
            for _ in range(0, color.square_count):
                x = random.randint(0, int(sector_size - 1 - size))
                y = random.randint(0, int(sector_size - 1 - size))
                output += "<rect "
                output += "fill=\"rgb(" + str(r) + ", " + str(g) + ", " + str(b) + ")\" "
                output += "height=\"" + str(size) + "\" width=\"" + str(size) + "\" "

                output += "x=\"" + str(sector.min_x + x) + "\" y=\"" + str(sector.min_y + y) + "\""
                output += "></rect>"

        self.output[1][len(self.output[1]) - 1] += output

    def write(self):
        file = open("output/output.html", "w")
        file.truncate()
        file.write(self.output[0] + "'" + ("', '".join(self.output[1])) + "'" + self.output[2])
        file.close()

        for generation in range(0, len(self.output[1])):
            file = open("output/output-{0}.svg".format(str(generation)), "w")
            file.truncate()
            file.write(
                '<svg baseProfile=\"tiny\" height=\"100%\" version=\"1.2\" width=\"100%\" '
                'xmlns=\"http://www.w3.org/2000/svg\" xmlns:ev=\"http://www.w3.org/2001/xml-events\" '
                'xmlns:xlink=\"http://www.w3.org/1999/xlink\" viewBox=\"0 0 1024 1024\"><defs />{0}</svg>'.format(
                    self.output[1][generation])
            )
            file.close()
