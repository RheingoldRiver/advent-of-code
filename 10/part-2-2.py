import json
import re
from copy import copy, deepcopy


class Solver:

    def __init__(self):
        with open('output_smaller.txt', 'r', encoding='utf-8') as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.data = [self.parse_line(line) for line in self.lines]

    def parse_line(self, line):
        return list(line)

    def run(self):
        total = 0
        for i, row in enumerate(self.data):
            for j, char in enumerate(row):
                inside_left = False
                inside_right = False
                inside_up = False
                inside_down = False
                if char == 'O':
                    continue
                for k in range(i):
                    if self.data[k][j] == 'O':
                        inside_up = True
                for k in range(j):
                    if self.data[i][k] == 'O':
                        inside_left = True
                for k in range(i, len(self.data)):
                    if self.data[k][j] == 'O':
                        inside_down = True
                for k in range(j, len(self.data[0])):
                    if self.data[i][k] == 'O':
                        inside_right = True
                if inside_up and inside_left and inside_right and inside_down:
                    print(f'found success: col {i} row {j}')
                    self.data[i][j] = 'X'
                    total += 1

        with open('part_2_output.txt', 'w') as f:
            f.write('\n'.join([''.join(row) for row in self.data]))

        return total


if __name__ == '__main__':
    print(Solver().run())
