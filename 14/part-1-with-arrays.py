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
            self.roll_rocks_in_col(col)
            for i, rock in enumerate(col.reversed()):
                if rock.value == 'O':
                    total += i + 1
        return total

    def roll_rocks_in_col(self, col):
        result = []
        for segment in col.string_and_split('#'):
            result.append(segment.replace('.', "") + segment.replace('O', ""))
        col.overwrite_values('#'.join(result))


if __name__ == '__main__':
    print(Solver().run())
