import functools
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
        one_group = [int(x) for x in line.split(' ')[1].split(',')]
        groups = one_group
        for i in range(4):
            groups = groups + copy(one_group)
        springs = line.split(' ')[0]
        contracted_springs = springs
        for _ in range(4):
            contracted_springs = f"{contracted_springs}?{springs}"
        return {
            'springs': contracted_springs,
            'groups': groups
        }
        # unknowns = []
        # broken = []
        # for i, val in enumerate(ret['springs']):
        #     if val == '?':
        #         unknowns.append(i)
        #     elif val == '#':
        #         broken.append(i)
        # ret['unknowns'] = unknowns
        # ret['broken'] = broken
        # ret['total'] = sum(ret['groups'])
        # ret['num_to_fill'] = ret['total'] - len(broken)
        # return ret

    def run(self):
        total = 0
        for line in self.data:
            cur_total = self.count_possibilities(line['springs'], tuple(line['groups']))
            total += cur_total
            line['cur_total'] = cur_total
            # print(line)

        return total

    @functools.cache
    def count_possibilities(self, springs, to_match):
        # print(f'springs: {str(springs)} to_match: {str(to_match)}')
        if len(to_match) == 0:
            if '#' not in springs:
                # print('haha yay we added something')
                return 1
            return 0
        if len(springs) == 0:
            return 0
        first_char = springs[0]
        next_match_size = to_match[0]
        if first_char == '.':
            # print('case 1')
            return self.count_possibilities(springs[1:], to_match)
        if first_char == '?':
            # print('case 2')
            case_where_broken = self.count_possibilities('#' + springs[1:], to_match)
            case_where_working = self.count_possibilities(springs[1:], to_match)
            return case_where_working + case_where_broken
        mandatory_chars = re.search(r'^(#+)', springs)[0]
        possible_chars = re.search(r'^([#?]+)', springs)[0]
        # print(f'mandatory: {mandatory_chars} possible: {possible_chars}')
        if len(possible_chars) < next_match_size:
            return 0
        if len(mandatory_chars) > next_match_size:
            return 0
        if len(springs) > next_match_size and springs[next_match_size] == '#':
            return 0
        return self.count_possibilities(springs[next_match_size + 1:], to_match[1:])

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
