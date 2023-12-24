import itertools
from typing import Optional

import numpy as np
from z3 import z3


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


class Solver:

    def __init__(self):
        with open('input.txt', 'r', encoding='utf-8') as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.data = [self.parse_line(i, line) for i, line in enumerate(self.lines)]

    def parse_line(self, i: int, line: str):
        p, v = line.split('@')
        return Line(p, v)

    def run(self):
        px = z3.BitVec('px', 50)
        py = z3.BitVec('py', 50)
        pz = z3.BitVec('pz', 50)
        vx = z3.BitVec('vx', 50)
        vy = z3.BitVec('vy', 50)
        vz = z3.BitVec('vz', 50)

        s = z3.Solver()

        for c, line in enumerate(self.data[:4]):
            t = z3.BitVec(f't{c}', 50)
            s.add(line.vx * t + line.px == vx * t + px)
            s.add(line.vy * t + line.py == vy * t + py)
            s.add(line.vz * t + line.pz == vz * t + pz)

        s.check()
        model = s.model()

        return sum(model[val].as_long() for val in [px, py, pz])


if __name__ == '__main__':
    print(Solver().run())
