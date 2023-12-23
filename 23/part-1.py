import json
import re
from copy import copy, deepcopy

import networkx
from networkx import dag_longest_path

from utils.grid.errors import MoveError
from utils.grid.grid import Grid
from utils.grid.pointer import Pointer


class Solver:

    def __init__(self):
        with open('input.txt', 'r', encoding='utf-8') as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.grid = Grid.read_from_lines(self.lines)
        self.graph = networkx.DiGraph()

    def run(self):
        graph = self.graph
        for cell in self.grid.all_grid_cells():
            self.graph.add_node(cell)
        ptr = self.grid.new_pointer()
        print(graph)

        for cell in self.grid.all_grid_cells():
            if cell.value == '#':
                continue
            ptr.move_to_cell(cell)
            if cell.value == '>':
                if ptr.can_move_right():
                    graph.add_edge(cell, ptr.peek_right(), weight=-1)
            elif cell.value == '<':
                if ptr.can_move_left():
                    graph.add_edge(cell, ptr.peek_left(), weight=-1)
            elif cell.value == 'v':
                if ptr.can_move_down():
                    graph.add_edge(cell, ptr.peek_down(), weight=-1)
            elif cell.value == '^':
                if ptr.can_move_up():
                    graph.add_edge(cell, ptr.peek_up(), weight=-1)
            else:
                for neighbor in ptr.current_neighbors():
                    if neighbor.value != '#':
                        graph.add_edge(cell, neighbor, weight=-1)

        print(graph)

        start = self.grid.cell_at(0, 1)
        the_end = self.grid.cell_at(self.grid.max_row, self.grid.max_col - 1)
        best = 0
        for path in networkx.all_simple_paths(graph, start, the_end):
            best = max(len(path) - 1, best)
        return best


if __name__ == '__main__':
    print(Solver().run())
