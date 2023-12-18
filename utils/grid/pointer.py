from copy import deepcopy
from typing import Optional, TYPE_CHECKING

from utils.grid.errors import PeekError, MoveError
from utils.grid.cell import Cell

if TYPE_CHECKING:
    from grid import Grid


class Direction:
    left = 'LEFT',
    right = 'RIGHT',
    up = 'UP',
    down = 'DOWN'

    @staticmethod
    def opposite(direction: "Direction"):
        if direction == Direction.left:
            return Direction.right
        if direction == Direction.right:
            return Direction.left
        if direction == Direction.up:
            return Direction.down
        if direction == Direction.down:
            return Direction.up


class Pointer:

    def __init__(self, grid: "Grid", idx, data=None):
        self.grid = grid
        self.row = 0
        self.col = 0
        self.id = idx
        self._ptr_data = data or {}

    def __str__(self):
        return f"<Ptr {self.id} at row {self.row} col {self.col}>"

    def __repr__(self):
        return f"<Ptr {self.id} at row {self.row} col {self.col}>"

    @property
    def cell(self) -> Cell:
        return self.grid.cell_at(self.row, self.col)

    @property
    def data(self):
        """Returns the full data dictionary at a cell, which may contain extra values."""
        return self.grid.data_at(self.row, self.col)

    @property
    def ptr_data(self):
        return self._ptr_data

    def set_ptr_data(self, new_data):
        self._ptr_data = new_data

    def update_ptr_data(self, new_data):
        self._ptr_data.update(new_data)

    def clone(self):
        new_ptr = self.grid.new_pointer(self.id + '2', deepcopy(self.ptr_data))
        new_ptr.move_to(self.row, self.col)
        return new_ptr

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

    def can_move_in_direction(self, direction, steps: int = 1):
        if direction == Direction.left:
            return self.can_move_left(steps)
        if direction == Direction.right:
            return self.can_move_right(steps)
        if direction == Direction.up:
            return self.can_move_up(steps)
        if direction == Direction.down:
            return self.can_move_down(steps)

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
                self.grid.update_indices()
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
                self.grid.update_indices()
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
                    self.grid.max_row + 1,
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
        if self.can_move_down(steps):
            ret.append(self.peek_down(steps, wrap))
        if self.can_move_up(steps):
            ret.append(self.peek_up(steps, wrap))
        if self.can_move_left(steps):
            ret.append(self.peek_left(steps, wrap))
        if self.can_move_right(steps):
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
