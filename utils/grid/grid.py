from copy import deepcopy
from typing import Generator, List

from utils.grid.Array import Array
from utils.grid.cell import Cell
from utils.grid.pointer import Pointer


class Grid:
    directions = [
        Cell(-1, 0),
        Cell(1, 0),
        Cell(0, -1),
        Cell(0, 1)
    ]

    directions_diagonal = [
        Cell(-1, -1),
        Cell(-1, 1),
        Cell(1, 1),
        Cell(1, -1)
    ]

    def __init__(self, grid):
        self.grid = grid

        self.min_row = 0
        self.min_col = 0
        self.is_infinite = False
        self.default_infinite_value = None
        self.infinite_update_indices = False
        self.directions_all = self.directions + self.directions_diagonal
        self.pointers = {}

    def __str__(self):
        return '\n'.join([''.join([str(c) for c in row]) for row in self.grid])

    def print_pointers(self):
        def char(row, col):
            for key, ptr in self.pointers.items():
                if ptr.row == row and ptr.col == col:
                    return key
            return '.'

        return '\n'.join([''.join([char(i, j) for j, c in enumerate(row)]) for i, row in enumerate(self.grid)])

    def new_pointer(self, key: str = None, data=None):
        if key is None:
            key = f"pointer{str(len(self.pointers.keys()))}"
        ptr = Pointer(self, key, data)
        self.pointers[key] = ptr
        return ptr

    def set_infinite(self, default_value=None, update_indices: bool = False):
        self.is_infinite = True
        self.default_infinite_value = default_value
        self.infinite_update_indices = update_indices

    @property
    def width(self):
        return len(self.grid[0])

    @property
    def height(self):
        return len(self.grid)

    @property
    def max_row(self):
        return self.height - 1

    @property
    def max_col(self):
        return self.width - 1

    def cell_at(self, row, col) -> Cell:
        return self.grid[row][col]

    def data_at(self, row, col):
        return self.grid[row][col].data

    def value_at(self, row, col):
        return self.grid[row][col].data['value']

    def update_data_at(self, row, col, new_data):
        self.data_at(row, col).update(new_data)

    def update_value_at(self, row, col, value):
        self.data_at(row, col).update({'value': value})

    @classmethod
    def read_from_lines(cls, lines, ints: bool = False) -> "Grid":
        grid = []
        for i, row in enumerate(lines):
            new_row = []
            grid.append(new_row)
            for j, cell in enumerate(row):
                new_row.append(Cell(i, j, {
                    'value': int(cell) if ints else cell
                }))
        return cls(grid)

    @classmethod
    def read_from_array(cls, array) -> "Grid":
        grid = []
        for i, row in enumerate(array):
            grid.append([Cell(i, j, {
                'value': val
            }) for j, val in enumerate(row)])
        return cls(grid)

    @classmethod
    def empty_grid(cls, num_rows, num_cols) -> "Grid":
        grid = []
        for i in range(num_rows):
            new_row = []
            grid.append(new_row)
            for j in range(num_cols):
                new_row.append(Cell(i, j, {
                    'value': None
                }))
        return cls(grid)

    def row_at(self, idx: int, as_copy: bool = True):
        if idx < 0:
            raise ValueError("requested row with index < 0")
        if idx >= self.height:
            raise ValueError("requested row with index > height")
        return Array(deepcopy(self.grid[idx]) if as_copy else self.grid[idx])

    def col_at(self, idx, as_copy: bool = True):
        if idx < 0:
            raise ValueError("requested column with index < 0")
        if idx >= self.width:
            raise ValueError("requested column with index > width")
        return Array([(deepcopy(row[idx]) if as_copy else row[idx]) for row in self.grid])

    def all_rows(self, as_copy: bool = True):
        for idx in range(len(self.grid)):
            yield self.row_at(idx, as_copy)

    def all_columns(self, as_copy: bool = True):
        for idx in range(len(self.grid[0])):
            yield self.col_at(idx, as_copy)

    def all_grid_cells(self) -> Generator[Cell, None, None]:
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                yield cell

    def grid_cells_with_value(self, value) -> Generator[Cell, None, None]:
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if cell.data['value'] == value:
                    yield cell

    def grid_cells_matching(self, f) -> Generator[Cell, None, None]:
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if f(cell):
                    yield cell

    def explode_rows(self, indices: List[int], times: int = 2):
        new_grid = []

        def add_row(row_index):
            new_row = []
            new_grid.append(new_row)
            for j, cell in enumerate(self.grid[row_index]):
                new_cell = deepcopy(cell)
                new_cell.data['original_row'] = row_index
                new_cell.data['original_col'] = j
                new_row.append(new_cell)

        for i, row in enumerate(self.grid):
            if i in indices:
                for _ in range(times):
                    add_row(i)
            else:
                add_row(i)
        self.grid = new_grid

    def explode_columns(self, indices: List[int], times: int = 2):
        new_grid = [[] for _ in range(len(self.grid))]

        def add_col(col_index):
            for i, row in enumerate(self.grid):
                new_cell = deepcopy(row[col_index])
                new_cell.data['original_row'] = i
                new_cell.data['original_col'] = col_index
                new_grid[i].append(new_cell)

        for j in range(len(self.grid[0])):
            if j in indices:
                for _ in range(times):
                    add_col(j)
            else:
                add_col(j)
        self.grid = new_grid


