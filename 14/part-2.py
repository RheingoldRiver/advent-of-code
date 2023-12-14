import json
import re
from copy import copy, deepcopy

from utils.grid.Array import Array
from utils.grid.grid import Grid


class Solver:

    def __init__(self):
        with open('input.txt', 'r', encoding='utf-8') as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.grid = Grid.read_from_lines(self.lines)

    def run(self):
        total = 0
        found_str = []
        weights = []
        while True:
            for col in self.grid.all_columns(False):
                self.roll_rocks_in_col(col, 'back')
                # print(str(self.grid))
                # print('********************************')
            for row in self.grid.all_rows(False):
                self.roll_rocks_in_col(row, 'back')
                # print(str(self.grid))
                # print('********************************')
            for col in self.grid.all_columns(False):
                self.roll_rocks_in_col(col, 'forward')
                # print(str(self.grid))
                # print('********************************')
            for row in self.grid.all_rows(False):
                self.roll_rocks_in_col(row, 'forward')
                # print(str(self.grid))
                # print('********************************')
            if (x := str(self.grid)) in found_str:
                print(found_str.index(x))
                break
            else:
                found_str.append(str(self.grid))
                weights.append(self.weight())
        print(weights)

    def roll_rocks_in_col(self, col: Array, direction):
        col_as_str = str(col)
        segments = col_as_str.split('#')
        result = []
        for segment in segments:
            if direction == 'back':
                result.append(segment.replace('.', "") + segment.replace('O', ""))
            else:
                result.append(segment.replace('O', "") + segment.replace('.', ""))
        full_result = '#'.join(result)
        for i, cell in enumerate(col):
            cell.set_value(full_result[i])

    def weight(self):
        total = 0
        # print(str(self.grid))
        for col in self.grid.all_columns():
            for i, rock in enumerate(col):
                if rock.value == 'O':
                    total += len(col) - i
        # print(total)
        return total


if __name__ == '__main__':
    print(Solver().run())
