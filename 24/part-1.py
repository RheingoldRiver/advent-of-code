import itertools
from typing import Optional

import numpy as np


class Line:
    def __init__(self, p, v):
        self.position = [int(x.strip()) for x in p.split(',')]
        self.velocity = [int(x.strip()) for x in v.split(',')]
        self.px = self.position[0]
        self.py = self.position[1]
        self.pz = self.position[2]
        self.vx = self.velocity[0]
        self.vy = self.velocity[1]
        self.vz = self.velocity[2]

    def __repr__(self):
        return f"<Line P {self.px} {self.py} {self.pz} V {self.vx} {self.vy} {self.vz}>"

    def solve_line(self, other: "Line") -> Optional["Point"]:
        A = np.array([[self.vx, -other.vx], [self.vy, -other.vy]])
        B = np.array([other.px - self.px, other.py - self.py])

        try:
            t, s = np.linalg.solve(A, B)

            x = self.px + self.vx * t
            y = self.py + self.vy * t
            if t >= 0 and s >= 0:
                return Point(x, y)
            return None
        except np.linalg.LinAlgError:
            return None

    def point_at(self, t):
        return Point(self.px + t * self.vx, self.py + t * self.py)


class Point:
    min = 200000000000000
    max = 400000000000000
    # min = 7
    # max = 27

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"<Point {self.x} {self.y}>"

    def in_bounds(self):
        return self.min <= self.x <= self.max and self.min <= self.y <= self.max


class Solver:

    def __init__(self):
        with open('input.txt', 'r', encoding='utf-8') as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.data = [self.parse_line(i, line) for i, line in enumerate(self.lines)]

    def parse_line(self, i: int, line: str):
        p, v = line.split('@')
        return Line(p, v)

    def run(self):
        total = 0
        for (a, b) in itertools.combinations(self.data, 2):
            res = a.solve_line(b)
            # print(res, res and res.in_bounds())
            if res is None:
                continue
            if res.in_bounds():
                total += 1
        return total


if __name__ == '__main__':
    print(Solver().run())
