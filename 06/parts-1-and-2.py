import json
from copy import copy


class Solver:

    def __init__(self):
        with open('info2.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def run(self):
        product = 1
        for race in self.data['races']:
            ways = 0
            for i in range(race['time']):
                if i * (race['time'] - i) > race['distance']:
                    ways += 1
            product *= max(ways, 1)
        return product


if __name__ == '__main__':
    print(Solver().run())
