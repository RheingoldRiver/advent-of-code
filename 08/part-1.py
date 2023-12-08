import json
import re
from copy import copy, deepcopy


class Solver:
    start = 'AAA'
    end = 'ZZZ'

    def __init__(self):
        with open('info.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        self.directions = self.data["line1"] * 20000
        self.resulting_options = [self.parse_line(line) for line in self.data["lookup"].split('\n')]
        self.lookup = {item['start']: item for item in self.resulting_options}

    @staticmethod
    def parse_line(line):
        start = line.split(' = ')[0]
        results = line.split(' = ')[1].replace('(', '').replace(')', '')
        return {
            'start': start,
            'L': results.split(', ')[0],
            'R': results.split(', ')[1],
        }

    def run(self):
        total = 0
        cur = self.start
        for char in self.directions:
            total += 1
            cur = self.lookup[cur][char]
            if cur == self.end:
                break

        return total


if __name__ == '__main__':
    print(Solver().run())
