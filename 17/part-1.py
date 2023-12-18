import json
import re
from collections import defaultdict
from copy import copy, deepcopy
from utils.grid.errors import MoveError
from utils.grid.grid import Grid
from utils.grid.pointer import Pointer, Direction


class Solver:
    max_in_a_direction = 3

    def __init__(self):
        with open('input.txt', 'r', encoding='utf-8') as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.grid = Grid.read_from_lines(self.lines, ints=True)

    def run(self):
        total = 0
        ptr = self.grid.new_pointer('path', {
            'cur_direction': Direction.right,
            'count': 0,
            'weight': 0,
        })
        ptr.move_to(0, 0)


        return total

    def step(self, ptr: Pointer):
        next_ptrs = []
        for next_dir in [Direction.left, Direction.right, Direction.up, Direction.down]:
            if ptr.ptr_data['count'] == self.max_in_a_direction and ptr.ptr_data['cur_direction'] != next_dir:
                continue
            if not ptr.can_move_in_direction(next_dir):
                continue
            if next_dir == Direction.opposite(next_dir):
                continue
            new_ptr = ptr.clone()
            data = new_ptr.ptr_data
            if data['cur_direction'] != next_dir:
                data['count'] += 1
            else:
                data['count'] = 0
                data['cur_direction'] = next_dir
                data['weight'] = data['weight'] + ptr.value


if __name__ == '__main__':
    print(Solver().run())
