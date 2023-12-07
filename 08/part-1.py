import json
import re
from copy import copy, deepcopy


class Solver:

    def __init__(self):
        with open('input.txt', 'r', encoding='utf-8') as f:
            self.lines = [line.strip() for line in f.readlines()]
        with open('info2.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def run(self):
        total = 0
        product = 1


        return total


if __name__ == '__main__':
    print(Solver().run())
