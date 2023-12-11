import json
import re
from copy import copy, deepcopy


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Solver:
    big_value = 1000000

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
        for i, point1 in enumerate(points_to_check):
            for point2 in points_to_check[i+1:]:
                total += abs(point2.y - point1.y) + abs(point2.x - point1.x)
        return total

    def expand(self):
        new_data = []
        for row in self.data:
            if all([x == '.' for x in row]):
                for i in range(self.big_value):
                    new_data.append(copy(row))
            else:
                new_data.append(copy(row))
        result = '\n'.join([''.join([str(c) for c in row]) for row in new_data])
        print(result)
        new_data2 = [[] for _ in range(len(new_data))]
        for j, _ in enumerate(new_data[0]):  # columns
            if all([_row[j] == '.' for _row in new_data]):
                print('found another column')
                for k in range(self.big_value):
                    for i, row in enumerate(new_data):
                        new_data2[i].append(row[j])
            else:
                for i, row in enumerate(new_data):
                    new_data2[i].append(row[j])
        return new_data2



if __name__ == '__main__':
    print(Solver().run())
