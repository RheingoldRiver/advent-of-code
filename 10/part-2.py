import json
import math
import re
from copy import copy, deepcopy
from typing import List


class InvalidPipe(ValueError):
    pass


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Solver:
    starting_char = 'J'
    adjacent_cells = [
        Point(0, -1),
        Point(0, 1),
        Point(1, 0),
        Point(-1, 0)
    ]

    def __init__(self):
        with open('input.txt', 'r', encoding='utf-8') as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.data = [['.'] * len(self.lines[0])] + [self.parse_line(line) for line in self.lines] + [
            ['.'] * len(self.lines[0])]
        print(self.data)
        self.start_y = -1
        self.start_x = -1
        self.initialize_starting_location()
        self.y = 0
        self.x = 0
        self.prev_y = 0
        self.prev_x = 0
        print(
            f'starting at: row {self.start_y} col {self.start_x} which is char {self.data[self.start_y][self.start_x]}')

        self.cleaned_data = [['.' for _ in range(len(self.data[1]) - 1)] for __ in range(len(self.data) - 1)]

    def initialize_starting_location(self):
        for i, line in enumerate(self.data):
            for j, char in enumerate(line):
                if char == 'S':
                    self.start_y = i
                    self.start_x = j

    def parse_line(self, line):
        ret = ['.'] + list(line) + ['.']
        return ret

    def increment_y(self, direction):
        cur_y = self.y
        self.y = cur_y + direction
        self.prev_y = cur_y
        self.prev_x = self.x

    def increment_x(self, direction):
        cur_x = self.x
        self.x = cur_x + direction
        self.prev_x = cur_x
        self.prev_y = self.y

    def consume_vertical(self):
        if self.prev_x != self.x:
            raise InvalidPipe
        self.increment_y(self.y - self.prev_y)

    def consume_horizontal(self):
        if self.prev_y != self.y:
            raise InvalidPipe
        self.increment_x(self.x - self.prev_x)

    def validate_from_point(self, point: Point):
        if self.y == self.prev_y + point.y and self.x == self.prev_x + point.x:
            return True
        return False

    def consume_L(self):
        if self.validate_from_point(Point(-1, 0)):
            self.increment_y(-1)
            return
        if self.validate_from_point(Point(0, 1)):
            self.increment_x(1)
            return
        raise InvalidPipe

    def consume_J(self):
        if self.validate_from_point(Point(1, 0)):
            self.increment_y(-1)
            return
        if self.validate_from_point(Point(0, 1)):
            self.increment_x(-1)
            return
        raise InvalidPipe

    def consume_7(self):
        if self.validate_from_point(Point(1, 0)):
            # print('7 from the left')
            self.increment_y(1)
            return
        if self.validate_from_point(Point(0, -1)):
            # print('7 from above')
            self.increment_x(-1)
            return
        # print(f'new x: {self.x} new y: {self.y}')
        raise InvalidPipe

    def consume_F(self):
        if self.validate_from_point(Point(-1, 0)):
            # print('F from the right')
            self.increment_y(1)
            return
        if self.validate_from_point(Point(0, -1)):
            # print('F from below')
            self.increment_x(1)
            return
        raise InvalidPipe

    def init(self, point: Point):
        self.prev_x = self.start_x
        self.prev_y = self.start_y
        self.x = self.start_x + point.x
        self.y = self.start_y + point.y

    def run_round(self):
        try:
            cleaned_data = deepcopy(self.cleaned_data)
            # print('*********New round********')
            count = 0
            while True:
                # print(f"x: {self.x}, y: {self.y}, count: {count}")
                count += 1
                char = self.data[self.y][self.x]
                cleaned_data[self.y][self.x] = char
                if char == '|':
                    # print('case |')
                    self.consume_vertical()
                elif char == '-':
                    # print('case -')
                    self.consume_horizontal()
                elif char == 'J':
                    # print('case J')
                    self.consume_J()
                elif char == 'L':
                    # print('case L')
                    self.consume_L()
                elif char == '7':
                    # print('case 7')
                    self.consume_7()
                elif char == 'F':
                    # print('case F')
                    self.consume_F()
                elif char == '.':
                    # print('reached the edge!')
                    raise InvalidPipe
                elif char == 'S':
                    # print('back to start!')
                    self.cleaned_data = cleaned_data
                    return math.ceil(count / 2)
                # print(f'next char: row {self.y} col {self.x} {self.data[self.y][self.x]}')
        except InvalidPipe:
            return -1

    def run(self):

        for starting_direction in [
            Point(-1, 0),
            Point(0, -1),
            Point(1, 0),
            Point(0, 1)
        ]:
            self.init(starting_direction)
            self.run_round()
        count = 0
        print('\n'.join([''.join(row) for row in self.cleaned_data]))
        new_data = []
        for i, row in enumerate(self.cleaned_data):
            cur_data = [
                [],
                [],
                []
            ]
            for cur_row in cur_data:
                new_data.append(cur_row)
            for j, char in enumerate(row):
                for cur_i, cur_row in enumerate(self.minigrid(char)):
                    for val in cur_row:
                        cur_data[cur_i].append(val)
        print('\n'.join([''.join([str(c) for c in row]) for row in new_data]))

        queue = [Point(0, 0)]
        while len(queue) > 0:
            cur_cell = queue.pop()
            for direction in self.adjacent_cells:
                next_cell = Point(cur_cell.x + direction.x, cur_cell.y + direction.y)
                if next_cell.x >= len(new_data[1]) or next_cell.x < 0:
                    continue
                if next_cell.y >= len(new_data) or next_cell.y < 0:
                    continue
                if new_data[next_cell.y][next_cell.x] == '.':
                    queue.append(next_cell)
                    new_data[next_cell.y][next_cell.x] = '0'
                if new_data[next_cell.y][next_cell.x] == '-':
                    queue.append(next_cell)
                    new_data[next_cell.y][next_cell.x] = '0'

        print('**********************************************************************************************')

        result = '\n'.join([''.join([str(c) for c in row]) for row in new_data])
        print(result)

        with open('output-2-actual.txt', 'w') as f:
            f.write(result)

        return count

    @staticmethod
    def minigrid(char):
        if char == '.':
            return [
                ['-', '-', '-'],
                ['-', '-', '-'],
                ['-', '-', '-'],
            ]
        elif char == '|':
            return [
                ['.', 1, '.'],
                ['.', 1, '.'],
                ['.', 1, '.']
            ]
        elif char == 'J':
            return [
                ['.', 1, '.'],
                [1, 1, '.'],
                ['.', '.', '.']
            ]
        elif char == '-':
            return [
                ['.', '.', '.'],
                [1, 1, 1],
                ['.', '.', '.'],
            ]
        elif char == '7':
            return [
                ['.', '.', '.'],
                [1, 1, '.'],
                ['.', 1, '.'],
            ]
        elif char == 'F' or char == 'S':
            return [
                ['.', '.', '.'],
                ['.', 1, 1],
                ['.', 1, '.']
            ]
        elif char == 'L':
            return [
                ['.', 1, '.'],
                ['.', 1, 1],
                ['.', '.', '.']
            ]


if __name__ == '__main__':
    print(Solver().run())
