import re


class Solver:
    colors = ['red', 'blue', 'green']
    color_pattern = '(\d+) {}'

    def __init__(self):
        with open('games.txt', 'r', encoding='utf-8') as f:
            self.lines = f.readlines()

    def run(self):
        total = 0
        for line in self.lines:
            product = 1
            for color in self.colors:
                product *= max([
                    int(i) for i in re.findall(self.color_pattern.format(color), line)])
            total += product

        return total

if __name__ == '__main__':
    print(Solver().run())