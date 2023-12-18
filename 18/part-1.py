import json
import re
from copy import copy, deepcopy

from utils.grid.cell import Cell
from utils.grid.errors import MoveError
from utils.grid.grid import Grid
from utils.grid.pointer import Pointer


class Solver:
    starting_pos_actual = Cell(row=209, col=128)
    starting_pos_test = Cell(row=1, col=1)

    def __init__(self):
        with open('input.txt', 'r', encoding='utf-8') as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.data = [self.parse_line(line) for line in self.lines]

    def parse_line(self, line):
        direction, steps, color = line.split(' ')
        color = color.replace('#', '').replace('(', '').replace(')', '')
        return {
            'direction': direction,
            'steps': int(steps),
            'color': color,
        }

    def run(self):
        grid = Grid.empty_grid(1, 1)
        grid.set_infinite(default_value='.', update_indices=True)
        pointer = grid.new_pointer()
        pointer.update_value('#')
        for line in self.data:
            steps = line['steps']
            if line['direction'] == 'U':
                for x in range(steps):
                    pointer.move_up(1)
                    pointer.update_value('#')
            if line['direction'] == 'D':
                for x in range(steps):
                    pointer.move_down(1)
                    pointer.update_value('#')
            if line['direction'] == 'R':
                for x in range(steps):
                    pointer.move_right(1)
                    pointer.update_value('#')
            if line['direction'] == 'L':
                for x in range(steps):
                    pointer.move_left(1)
                    pointer.update_value('#')
        print(str(grid))

        pathfinder = grid.new_pointer()
        start_at = self.starting_pos_actual
        queue = [start_at]

        grid.update_indices()

        # for cell in grid.all_grid_cells():
        #     print(cell.row, cell.col, cell.value)

        while len(queue) > 0:
            cur_point = queue.pop()
            pathfinder.move_to(cur_point.row, cur_point.col)
            for cell in pathfinder.current_neighbors():
                if cell.value == '#' or cell.value == 'X':
                    continue
                cell.set_value('X')
                queue.append(cell)


        total = 0
        for cell in grid.grid_cells_matching(lambda x: x.value == 'X' or x.value == '#'):
            total += 1


        return total


if __name__ == '__main__':
    print(Solver().run())
