import json
import re
from copy import copy, deepcopy


class Solver:

    def __init__(self):
        with open('input.txt', 'r', encoding='utf-8') as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.data = [self.parse_line(line) for line in self.lines]

    @staticmethod
    def parse_line(line):
        new_line = [int(i) for i in line.split(' ')]
        new_line.reverse()
        return new_line

    def run(self):
        total = 0
        for line in self.data:
            print(f"New line: {str(line)}")
            differences = []
            current = copy(line)
            while any([i != 0 for i in current]):
                new = []
                for i, x in enumerate(current):
                    if i == 0:
                        continue
                    new.append(x - current[i-1])
                differences.append(current[-1])
                current = new
                print(current)
            differences.reverse()
            total += sum(*[differences])

        return total


if __name__ == '__main__':
    print(Solver().run())
