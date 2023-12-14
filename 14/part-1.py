import json
import re
from copy import copy, deepcopy

from utils.grid.grid import Grid


class Solver:

    def __init__(self):
        with open('input.txt', 'r', encoding='utf-8') as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.grid = Grid.read_from_lines(self.lines)

    def run(self):
        total = 0
        for col in self.grid.all_columns():
            new_col = self.roll_rocks_in_col(col)
            print(new_col)
            for i, rock in enumerate(new_col):
                if rock == 'O':
                    total += len(col) - i
        return total

    def roll_rocks_in_col(self, col):
        col_as_str = str(col)
        segments = col_as_str.split('#')
        result = []
        for segment in segments:
            result.append(segment.replace('.', "") + segment.replace('O', ""))
        return '#'.join(result)


if __name__ == '__main__':
    print(Solver().run())
