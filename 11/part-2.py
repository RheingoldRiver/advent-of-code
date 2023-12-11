import json
import re
from copy import copy, deepcopy


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Solver:

    def __init__(self):
        with open('input.txt', 'r', encoding='utf-8') as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.data = [self.parse_line(line) for line in self.lines]

    def parse_line(self, line):
        return list(line)

    def run(self):
        new_data = self.expand()
        result = '\n'.join([''.join([str(c) for c in row]) for row in new_data])
        print(result)
        total = 0
        points_to_check = []
        for i, row in enumerate(new_data):
            for j, cell in enumerate(row):
                if cell == '#':
                    points_to_check.append(Point(j, i))
        pairs_checked = 0
        for i, point1 in enumerate(points_to_check):
            for j, point2 in enumerate(points_to_check[i+1:]):
                pairs_checked += 1
                cur_total = 0
                for y_coord in self.get_range(point1.y, point2.y):
                    if new_data[y_coord][0] == '-':
                        # print(f'y case {y_coord} -')
                        cur_total += 1000000
                    else:
                        # print(f'y case {y_coord}')
                        cur_total += 1
                for x_coord in self.get_range(point1.x, point2.x):
                    if new_data[0][x_coord] == '-':
                        # print(f'x case {x_coord} -')
                        cur_total += 1000000
                    else:
                        # print(f'x case {x_coord}')
                        cur_total += 1
                total += cur_total
        print(f"pairs checked: {pairs_checked}")
        return total

    def get_range(self, p1, p2):
        return range(min(p1, p2), max(p1, p2))

    def expand(self):
        new_data = []
        for row in self.data:
            if all([x == '.' for x in row]):
                new_data.append(self.empty_line(len(row)))
            else:
                new_data.append(copy(row))
        result = '\n'.join([''.join([str(c) for c in row]) for row in new_data])
        print(result)
        new_data2 = [[] for _ in range(len(new_data))]
        print(new_data2)
        for j, _ in enumerate(new_data[0]):  # columns
            if all([(_row[j] == '.' or _row[j] == '-') for _row in new_data]):
                for i, row in enumerate(new_data):
                    new_data2[i].append('-')
            else:
                for i, row in enumerate(new_data):
                    new_data2[i].append(row[j])
        return new_data2

    def empty_line(self, num):
        return ['-'] * num


if __name__ == '__main__':
    print(Solver().run())
