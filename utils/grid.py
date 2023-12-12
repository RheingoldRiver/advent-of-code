from copy import deepcopy
from typing import Generator, List, Optional


class MoveError(ValueError):
    pass


class PeekError(ValueError):
    pass


class Cell:
    def __init__(self, row: int, col: int, data=None):
        self.row = row
        self.col = col
        self.data = data

    def __repr__(self):
        return f"<Point {str(self.data)} at row {self.row} col {self.col}>"

    def __str__(self):
        return str(self.data['value'])


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

    def new_pointer(self, key: str = None):
        if key is None:
            key = f"pointer{str(len(self.pointers.keys()))}"
        ptr = Pointer(self, key)
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
    def read_from_lines(cls, lines) -> "Grid":
        grid = []
        for i, row in enumerate(lines):
            new_row = []
            grid.append(new_row)
            for j, cell in enumerate(row):
                new_row.append(Cell(i, j, {
                    'value': cell
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
        return deepcopy(self.grid[idx]) if as_copy else self.grid[idx]

    def col_at(self, idx, as_copy: bool = True):
        if idx < 0:
            raise ValueError("requested column with index < 0")
        if idx >= self.width:
            raise ValueError("requested column with index > width")
        return [(deepcopy(row[idx]) if as_copy else row[idx]) for row in self.grid]

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


class Pointer:
    def __init__(self, grid: Grid, idx):
        self.grid = grid
        self.row = 0
        self.col = 0
        self.id = idx

    def __str__(self):
        return f"<Ptr {self.id} at row {self.row} col {self.col}>"

    @property
    def cell(self) -> Cell:
        return self.grid.cell_at(self.row, self.col)

    @property
    def data(self):
        """Returns the full data dictionary at a cell, which may contain extra values."""
        return self.grid.data_at(self.row, self.col)

    @property
    def value(self):
        """Returns the constant value of `data.value` at the current location"""
        return self.grid.value_at(self.row, self.col)

    def update_data(self, new_data):
        self.grid.update_data_at(self.row, self.col, new_data)

    def update_value(self, value):
        self.grid.update_value_at(self.row, self.col, value)

    def taxicab(self, other: "Pointer") -> int:
        return abs(self.row - other.row) + abs(self.col - other.col)

    def taxicab_with_diagonals(self, other: "Pointer") -> int:
        return max(abs(self.row - other.row), abs(self.col - other.col))

    def horizontal_dist(self, other: "Pointer") -> int:
        return abs(self.col - other.col)

    def vertical_dist(self, other: "Pointer") -> int:
        return abs(self.row - other.row)

    def move_in_direction_of(self, other: "Pointer", steps: int = 1):
        if other.col < self.col:
            self.move_left(steps)
        elif other.col > self.col:
            self.move_right(steps)

        if other.row < self.row:
            self.move_up(steps)
        elif other.row > self.row:
            self.move_down(steps)

    def move_to(self, row, col):
        self.col = col
        self.row = row

    def can_move_right(self, steps: int = 1):
        return self.col <= self.grid.width - 1 - steps

    def can_move_left(self, steps: int = 1):
        return self.col >= 0 + steps

    def can_move_up(self, steps: int = 1):
        return self.row >= 0 + steps

    def can_move_down(self, steps: int = 1):
        return self.row <= self.grid.height - 1 - steps

    def can_move_up_left(self, steps_up: int = 1, steps_left: int = 1):
        return self.can_move_left(steps_left) and self.can_move_up(steps_up)

    def can_move_up_right(self, steps_up: int = 1, steps_right: int = 1):
        return self.can_move_right(steps_right) and self.can_move_up(steps_up)

    def can_move_down_left(self, steps_down: int = 1, steps_left: int = 1):
        return self.can_move_left(steps_left) and self.can_move_down(steps_down)

    def can_move_down_right(self, steps_down: int = 1, steps_right: int = 1):
        return self.can_move_right(steps_right) and self.can_move_down(steps_down)

    @property
    def steps_to_right_edge(self):
        return self.grid.max_col - self.col

    @property
    def steps_to_left_edge(self):
        return self.col - 0

    @property
    def steps_to_top_edge(self):
        return self.row - 0

    @property
    def steps_to_bottom_edge(self):
        return self.grid.max_row - self.row

    def coord_right(self, steps: int = 1, wrap: bool = False):
        if self.can_move_right(steps):
            return self.col + steps
        elif wrap:
            return (self.col + steps) % self.grid.width
        else:
            return None

    def coord_left(self, steps: int = 1, wrap: bool = False):
        if self.can_move_left(steps):
            return self.col - steps
        elif wrap:
            return (self.col - steps) % self.grid.width
        else:
            return None

    def coord_up(self, steps: int = 1, wrap: bool = False):
        if self.can_move_up(steps):
            return self.row - steps
        elif wrap:
            return (self.row - steps) % self.grid.height
        else:
            return None

    def coord_down(self, steps: int = 1, wrap: bool = False):
        if self.can_move_down(steps):
            return self.row + steps
        elif wrap:
            return (self.row + steps) % self.grid.height
        else:
            return None

    def update_indices_on_insert(self, min_row: Optional[int] = None, min_col: Optional[int] = None):
        for i in range(min_row or 0, self.grid.height):
            for j in range(min_col or 0, self.grid.width):
                self.grid.cell_at(i, j).row = i
                self.grid.cell_at(i, j).col = j

    def move_right(self, steps: int = 1, wrap: bool = False):
        if (new_col := self.coord_right(steps, wrap)) is not None:
            self.col = new_col
        elif self.grid.is_infinite:
            for _ in range(steps - (self.grid.max_col - self.col)):
                for i, row in enumerate(self.grid.grid):
                    row.append(Cell(i, len(row), {
                        'value': self.grid.default_infinite_value
                    }))
            self.col = self.grid.max_col
        else:
            raise MoveError("Cannot move right!")

    def peek_right(self, steps: int = 1, wrap: bool = False) -> Cell:
        if (new_col := self.coord_right(steps, wrap)) is not None:
            return self.grid.cell_at(self.row, new_col)
        else:
            raise PeekError("Cannot peek right!")

    def move_left(self, steps: int = 1, wrap: bool = False):
        if (new_col := self.coord_left(steps, wrap)) is not None:
            self.col = new_col
        elif self.grid.is_infinite:
            num_to_add = steps - (self.col - self.grid.min_col)
            for _ in range(num_to_add):
                for i, row in enumerate(self.grid.grid):
                    row.insert(0, Cell(0, i, {
                        'value': self.grid.default_infinite_value
                    }))
            if self.grid.infinite_update_indices:
                self.update_indices_on_insert()
            self.col = self.grid.min_col
            for idx, ptr in self.grid.pointers.items():
                if idx != self.id:
                    ptr.move_right(num_to_add)
        else:
            raise MoveError("Cannot move left!")

    def peek_left(self, steps: int = 1, wrap: bool = False) -> Cell:
        if (new_col := self.coord_left(steps, wrap)) is not None:
            return self.grid.cell_at(self.row, new_col)
        else:
            raise PeekError("Cannot peek left!")

    def move_up(self, steps: int = 1, wrap: bool = False):
        if (new_row := self.coord_up(steps, wrap)) is not None:
            self.row = new_row
        elif self.grid.is_infinite:
            num_to_add = steps - (self.row - self.grid.min_row)
            for _ in range(num_to_add):
                new_row = [Cell(
                    0,
                    j,
                    {'value': self.grid.default_infinite_value}) for j in range(self.grid.width)]
                self.grid.grid.insert(0, new_row)
            if self.grid.infinite_update_indices:
                self.update_indices_on_insert()
            self.row = self.grid.min_row
            for idx, ptr in self.grid.pointers.items():
                if idx != self.id:
                    ptr.move_down(num_to_add)
        else:
            raise MoveError("Cannot move up!")

    def peek_up(self, steps: int = 1, wrap: bool = False) -> Cell:
        if (new_row := self.coord_up(steps, wrap)) is not None:
            return self.grid.cell_at(new_row, self.col)
        else:
            raise PeekError("Cannot peek up!")

    def move_down(self, steps: int = 1, wrap: bool = False):
        if (new_row := self.coord_down(steps, wrap)) is not None:
            self.row = new_row
        elif self.grid.is_infinite:
            for _ in range(steps - (self.grid.max_row - self.row)):
                new_row = [Cell(
                    0,
                    j,
                    {'value': self.grid.default_infinite_value}) for j in range(self.grid.width)]
                self.grid.grid.append(new_row)
            self.row = self.grid.max_row
        else:
            raise MoveError("Cannot move down!")

    def peek_down(self, steps: int = 1, wrap: bool = False) -> Cell:
        if (new_row := self.coord_down(steps, wrap)) is not None:
            return self.grid.grid[new_row][self.col]
        else:
            raise PeekError("Cannot peek down!")

    def peek_down_right(self, steps_down: int = 1, steps_right: int = 1, wrap: bool = False):
        if ((new_row := self.coord_down(steps_down, wrap)) is not None
                and (new_col := self.coord_right(steps_right, wrap)) is not None):
            return self.grid.grid[new_row][new_col]
        else:
            raise PeekError("Cannot peek down-right!")

    def peek_up_right(self, steps_up: int = 1, steps_right: int = 1, wrap: bool = False):
        if ((new_row := self.coord_up(steps_up, wrap)) is not None
                and (new_col := self.coord_right(steps_right, wrap)) is not None):
            return self.grid.grid[new_row][new_col]
        else:
            raise PeekError("Cannot peek up-right!")

    def peek_up_left(self, steps_up: int = 1, steps_left: int = 1, wrap: bool = False):
        if ((new_row := self.coord_up(steps_up, wrap)) is not None
                and (new_col := self.coord_left(steps_left, wrap)) is not None):
            return self.grid.grid[new_row][new_col]
        else:
            raise PeekError("Cannot peek up-left!")

    def peek_down_left(self, steps_down: int = 1, steps_left: int = 1, wrap: bool = False):
        if ((new_row := self.coord_down(steps_down, wrap)) is not None
                and (new_col := self.coord_left(steps_left, wrap)) is not None):
            return self.grid.grid[new_row][new_col]
        else:
            raise PeekError("Cannot peek down-left!")

    def move_down_right(self, steps_down: int = 1, steps_right: int = 1, wrap: bool = False):
        if self.can_move_down(steps_down) and self.can_move_right(steps_right):
            self.move_down(steps_down)
            self.move_right(steps_right)
        elif wrap:
            self.move_down(steps_down, wrap)
            self.move_right(steps_right, wrap)
        elif not self.can_move_right(steps_right) and not self.can_move_down(steps_down):
            raise MoveError("Cannot move down or right!")
        elif not self.can_move_right(steps_right):
            raise MoveError("Cannot move right!")
        elif not self.can_move_down(steps_down):
            raise MoveError("Cannot move down!")

    def move_up_right(self, steps_up: int = 1, steps_right: int = 1, wrap: bool = False):
        if self.can_move_up(steps_up) and self.can_move_right(steps_right):
            self.move_up(steps_up)
            self.move_right(steps_right)
        elif wrap:
            self.move_up(steps_up, wrap)
            self.move_right(steps_right, wrap)
        elif not self.can_move_right(steps_right) and not self.can_move_up(steps_up):
            raise MoveError("Cannot move up or right!")
        elif not self.can_move_right(steps_right):
            raise MoveError("Cannot move right!")
        elif not self.can_move_up(steps_up):
            raise MoveError("Cannot move up!")

    def move_up_left(self, steps_up: int = 1, steps_left: int = 1, wrap: bool = False):
        if self.can_move_up(steps_up) and self.can_move_left(steps_left):
            self.move_up(steps_up)
            self.move_left(steps_left)
        elif wrap:
            self.move_up(steps_up, wrap)
            self.move_left(steps_left, wrap)
        elif not self.can_move_left(steps_left) and not self.can_move_up(steps_up):
            raise MoveError("Cannot move up or left!")
        elif not self.can_move_left(steps_left):
            raise MoveError("Cannot move left!")
        elif not self.can_move_up(steps_up):
            raise MoveError("Cannot move up!")

    def move_down_left(self, steps_down: int = 1, steps_left: int = 1, wrap: bool = False):
        if self.can_move_down(steps_down) and self.can_move_left(steps_left):
            self.move_down(steps_down)
            self.move_left(steps_left)
        elif wrap:
            self.move_down(steps_down, wrap)
            self.move_left(steps_left, wrap)
        elif not self.can_move_left(steps_left) and not self.can_move_down(steps_down):
            raise MoveError("Cannot move down or left!")
        elif not self.can_move_left(steps_left):
            raise MoveError("Cannot move left!")
        elif not self.can_move_down(steps_down):
            raise MoveError("Cannot move down!")

    def current_neighbors(self, steps: int = 1, wrap: bool = False):
        ret = []
        if self.can_move_down():
            ret.append(self.peek_down(steps, wrap))
        if self.can_move_up():
            ret.append(self.peek_up(steps, wrap))
        if self.can_move_left():
            ret.append(self.peek_left(steps, wrap))
        if self.can_move_right():
            ret.append(self.peek_right(steps, wrap))
        return ret

    def current_diagonal_neighbors(self, steps_vertical: int = 1, steps_horitzontal: int = 1, wrap: bool = False):
        ret = []
        if self.can_move_down_right():
            ret.append(self.peek_down_right(steps_vertical, steps_horitzontal, wrap))
        if self.can_move_down_left():
            ret.append(self.peek_down_left(steps_vertical, steps_horitzontal, wrap))
        if self.can_move_up_right():
            ret.append(self.peek_up_right(steps_vertical, steps_horitzontal, wrap))
        if self.can_move_up_left():
            ret.append(self.peek_up_left(steps_vertical, steps_horitzontal, wrap))
        return ret

    def all_current_neighbors(self, steps: int = 1, wrap: bool = False):
        return self.current_neighbors(steps, wrap) + self.current_diagonal_neighbors(steps, steps, wrap)
