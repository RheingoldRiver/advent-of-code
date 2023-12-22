import json
import re
from copy import copy, deepcopy
from utils.grid.errors import MoveError
from utils.grid.grid import Grid
from utils.grid.pointer import Pointer


class Cube:
    def __init__(self, x, y, brick: "Brick"):
        self.x = x
        self.y = y
        self.brick = brick

    def __repr__(self):
        return f"<Cube {self.brick.id}: {str(self.x)}, {str(self.y)}, {str(self.z)}>"


class Brick:

    def __repr__(self):
        x = f"{str(self.x_dims[0])}-{str(self.x_dims[1])}" if self.direction == 'X' else str(self.x_dims[0])
        y = f"{str(self.y_dims[0])}-{str(self.y_dims[1])}" if self.direction == 'Y' else str(self.y_dims[0])
        z = f"{str(self.z_dims[0])}-{str(self.z_dims[1])}" if self.direction == 'Z' else str(self.z_dims[0])
        return f"<Brick {self.id}: x: {x} y: {y} @ {self.min_z} to {self.max_z}>"

    def __init__(self, c1, c2, idx):
        self.id = idx
        self.starting_coords = [[int(i) for i in c1.split(',')], [int(i) for i in c2.split(',')]]
        self.x_dims = [x[0] for x in self.starting_coords]
        if self.x_dims[0] > self.x_dims[1]:
            self.x_dims.reverse()
        self.y_dims = [x[1] for x in self.starting_coords]
        if self.y_dims[0] > self.y_dims[1]:
            self.y_dims.reverse()
        self.z_dims = [x[2] for x in self.starting_coords]
        if self.z_dims[0] > self.z_dims[1]:
            self.z_dims.reverse()
        self.min_z = self.z_dims[0]
        self.max_z = self.z_dims[1]
        self._dimensions = {
            'X': self.x_dims,
            'Y': self.y_dims,
            'Z': self.z_dims
        }
        self.bricks_below = []
        self.bricks_above = []

    def add_brick_below(self, brick: "Brick"):
        self.bricks_below.append(brick)

    def add_brick_above(self, brick: "Brick"):
        self.bricks_above.append(brick)

    def set_min_z(self, z):
        delta = z - self.min_z
        self.min_z = z
        self.max_z = self.max_z + delta

    @property
    def direction(self):
        for k, v in self._dimensions.items():
            if v[0] != v[1]:
                return k
        return 'Z'

    @property
    def occupied_squares(self):
        if self.direction == 'X':
            for x in range(self.x_dims[0], self.x_dims[1] + 1):
                yield Cube(x, self.y_dims[0], self)
        elif self.direction == 'Y':
            for y in range(self.y_dims[0], self.y_dims[1] + 1):
                yield Cube(self.x_dims[0], y, self)
        else:
            raise ValueError('should not be looking for occupied squares in z direction')

    @property
    def dependents(self):
        disintegrated = []
        queue = [self]
        while len(queue) > 0:
            cur = queue.pop(0)
            disintegrated.append(cur)
            for above_brick in cur.bricks_above:
                if all([b in disintegrated for b in above_brick.bricks_below]):
                    if above_brick not in disintegrated and above_brick not in queue:
                        queue.append(above_brick)
        return disintegrated


class Solver:

    def __init__(self):
        with open('input.txt', 'r', encoding='utf-8') as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.data: list[Brick] = [self.parse_line(i, line) for i, line in enumerate(self.lines)]
        self.grid = Grid.empty_grid(10, 10)

    def parse_line(self, i, line) -> Brick:
        p1, p2 = line.split('~')
        return Brick(p1, p2, i)

    def populate_grid(self):
        for brick in sorted(self.data, key=lambda x: x.z_dims[0]):
            if brick.direction == 'Z':
                assert brick.x_dims[0] == brick.x_dims[1]
                assert brick.y_dims[0] == brick.y_dims[1]
                cur_data = self.grid.data_at(brick.x_dims[0], brick.y_dims[0])
                brick.set_min_z(cur_data['height'] + 1)
                cur_data['height'] = brick.max_z
                stack = cur_data['stack']
                if len(stack) > 0:
                    prev_brick_here: Brick = stack[len(stack) - 1]
                    brick.add_brick_below(prev_brick_here)
                    prev_brick_here.add_brick_above(brick)
                stack.append(brick)
                continue

            assert brick.z_dims[0] == brick.z_dims[1]
            max_prev_height = 0
            for square in brick.occupied_squares:
                max_prev_height = max(self.grid.data_at(square.x, square.y)['height'], max_prev_height)
            brick.set_min_z(max_prev_height + 1)
            for square in brick.occupied_squares:
                cur_data = self.grid.data_at(square.x, square.y)
                cur_data['height'] = brick.max_z
                stack = cur_data['stack']
                if len(stack) > 0:
                    prev_brick_here: Brick = stack[len(stack) - 1]
                    if prev_brick_here.max_z == max_prev_height:
                        brick.add_brick_below(prev_brick_here)
                        prev_brick_here.add_brick_above(brick)
                stack.append(brick)

    def run(self):
        for cell in self.grid.all_grid_cells():
            cell.data = {
                'height': 0,
                'stack': [],
            }
        self.populate_grid()
        total = 0
        for brick in self.data:
            total += len(brick.dependents) - 1

        return total


if __name__ == '__main__':
    print(Solver().run())
