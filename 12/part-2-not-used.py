import itertools
import json
import math
import re
from copy import copy, deepcopy
from functools import reduce


class Solver:
    conditions = {
        '.': "operational",
        '?': "unknown",
        "#": 'damaged',
    }

    def __init__(self):
        with open('one_line.txt', 'r', encoding='utf-8') as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.data = [self.parse_line(line) for line in self.lines]

    def parse_line(self, line):
        ret = {
            "groups": [int(x) for x in line.split(' ')[1].split(',')],
        }
        springs = str(line.split(' ')[0])
        # print(springs)
        for i in range(4):
            springs = f"{springs}?{springs}"
        # print(springs)
        contracted_springs = re.sub(r'\.{2,}', '.', springs)
        # print(contracted_springs)
        ret['springs'] = [list(spring) for spring in contracted_springs.split('.')]
        ret['groups'] = ret['groups'] * 5
        unknowns = []
        broken = []
        for i, val in enumerate(ret['springs']):
            if val == '?':
                unknowns.append(i)
            elif val == '#':
                broken.append(i)
        ret['unknowns'] = unknowns
        ret['broken'] = broken
        ret['total'] = sum(ret['groups'])
        ret['num_to_fill'] = ret['total'] - len(broken)
        return ret

    def run(self):
        total = 0
        for line in self.data:
            cur_total = self.count_subset(line['springs'], line['groups'])
            line['cur_total'] = cur_total
            print(line)
            total += cur_total

        return total

    def count_subset(self, subset, what_to_put_here):
        if len(subset) <= 1 or len(what_to_put_here) <= 1:
            return self.bruteforce(subset, what_to_put_here)

        # if num_items_to_place == 1:
        #     ways = 0
        #     return ways
        # if len(subset) == 1:
        #     return math.comb(len(subset[0]) - num_occupied_cells, num_whitespace_spots)
        for x in range(0, len(subset)):
            for y in range(0, len(what_to_put_here)):
                cur_total = 0
                if 
                return self.count_subset(subset[:x], what_to_put_here[:y]) + self.count_subset(subset[x:], what_to_put_here[:y]) + self.count_subset(subset[:x], what_to_put_here[y:]) + self.count_subset(subset[x:], what_to_put_here[y:])

    def bruteforce(self, subset, what_to_put_here):
        print(subset)
        print(what_to_put_here)
        springs = list(''.join([''.join(x) for x in subset]))
        unknowns = []
        broken = []
        for i, val in enumerate(springs):
            if val == '?':
                unknowns.append(i)
            elif val == '#':
                broken.append(i)
        total_to_find = sum(what_to_put_here)
        num_to_fill = total_to_find - len(broken)
        if num_to_fill < 1:
            return 0

        cur_total = 0
        for possible_set in itertools.combinations(unknowns, num_to_fill):
            new_springs = copy(springs)
            for i in list(possible_set):
                new_springs[i] = '#'
            # print(possible_set)
            # print(new_springs)
            if self.valid(new_springs, what_to_put_here):
                cur_total += 1

        return cur_total


    def valid(self, possible_row, groups):
        actual_groups = []
        current_group = 0
        for cell in possible_row:
            if (cell == '.' or cell == '?') and current_group > 0:
                actual_groups.append(current_group)
                current_group = 0
            elif cell == '.' or cell == '?':
                continue
            elif cell == '#':
                current_group += 1
            # else:
            #     raise ValueError(f"unexpected character {cell} in row {possible_row}")
        if current_group > 0:
            actual_groups.append(current_group)
        return actual_groups == groups


if __name__ == '__main__':
    print(Solver().run())
