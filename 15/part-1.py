import json
import re
from copy import copy, deepcopy


class Solver:

    def __init__(self):
        with open('test.txt', 'r', encoding='utf-8') as f:
            self.raw_input = [line.strip() for line in f.readlines()]
        self.data = self.raw_input[0].split(',')
        self.boxes = {}
        for i in range(225):
            self.boxes[i] = {
                'lenses': [],
                'labels': [],
            }

    def run(self):

        total = 0
        for step in self.data:
            total += self.get_hash(step)

        return total

    def get_hash(self, step):
        cur_value = 0
        for char in step:
            cur_value += ord(char)
            cur_value *= 17
            cur_value = cur_value % 256
        return cur_value


if __name__ == '__main__':
    print(Solver().run())
