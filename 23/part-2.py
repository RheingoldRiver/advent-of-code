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
        self.graph = networkx.Graph()

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
            for neighbor in ptr.current_neighbors(wall='#'):
                graph.add_edge(cell, neighbor, weight=1)

        print(graph)

        while True:
            did_something = False
            for node in graph.nodes:
                if len(graph[node]) != 2:
                    continue
                (node1, data1), (node2, data2) = graph[node].items()
                did_something = True
                new_wt = data1['weight'] + data2['weight']
                graph.remove_edge(node, node1)
                graph.remove_edge(node, node2)
                graph.add_edge(node1, node2, weight=new_wt)
            if not did_something:
                break

        print(graph)
        start = self.grid.cell_at(0, 1)
        the_end = self.grid.cell_at(self.grid.max_row, self.grid.max_col - 1)
        best = 0
        for path in networkx.all_simple_paths(graph, start, the_end):
            cur = 0
            for i, node in enumerate(path):
                if i == 0:
                    continue
                cur += graph.edges[path[i-1], node]['weight']
            best = max(cur, best)
        return best


if __name__ == '__main__':
    print(Solver().run())
