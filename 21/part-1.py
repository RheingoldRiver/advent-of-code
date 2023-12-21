import json
import re
from copy import copy, deepcopy
from utils.grid.errors import MoveError
from utils.grid.grid import Grid
from utils.grid.pointer import Pointer

class Solver:

    def __init__(self):
        with open('input.txt', 'r', encoding='utf-8') as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.grid = Grid.read_from_lines(self.lines)

    def parse_line(self, line):
        return {

        }

    def run(self):
        total = 0
        first_pointer = self.grid.new_pointer()
        first_pointer.move_to_value('S')
        queue = [first_pointer]
        for i in range(64):
            next_queue = []
            found_cells = []
            for ptr in queue:
                for cell in ptr.current_neighbors(wrap=True):
                    if cell.value == '#':
                        continue
                    if cell in found_cells:
                        continue
                    found_cells.append(cell)
                    new_ptr = ptr.clone()
                    new_ptr.move_to(cell.row, cell.col)
                    next_queue.append(new_ptr)
            queue = next_queue
        return len(queue)


if __name__ == '__main__':
    print(Solver().run())
