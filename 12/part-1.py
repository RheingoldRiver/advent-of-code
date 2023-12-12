import itertools
import json
import re
from copy import copy, deepcopy



class Solver:
    conditions = {
        '.': "operational",
        '?': "unknown",
        "#": 'damaged',
    }

    def __init__(self):
        with open('input.txt', 'r', encoding='utf-8') as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.data = [self.parse_line(line) for line in self.lines]

    def parse_line(self, line):
        ret = {
            "springs": list(line.split(' ')[0]),
            "groups": [int(x) for x in line.split(' ')[1].split(',')],
        }
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
            cur_total = 0
            for possible_set in itertools.combinations(line['unknowns'], line['num_to_fill']):
                new_springs = copy(line['springs'])
                for i in list(possible_set):
                    new_springs[i] = '#'
                # print(possible_set)
                # print(new_springs)
                if self.valid(new_springs, line['groups']):
                    cur_total += 1
                line['total'] = cur_total
            total += cur_total
            # print(line)

        return total

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
