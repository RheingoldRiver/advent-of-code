import json
import re
from copy import deepcopy


class Instruction:
    noop = "PASS_THROUGH"
    accept = 'ACCEPT'
    reject = "REJECT"

    def __init__(self, kind: str = '', op: str = '', limit: str = '0', res: str = ''):
        self.kind = kind
        self.op = op
        self.limit = int(limit)
        self.res = res

    def __repr__(self):
        return f"<Instruction {self.kind} {self.op} {self.limit} -> {self.res}>"

    def do_op(self, item: int, limit: int):
        if self.op == '<' and item < limit:
            return True
        if self.op == '>' and item > limit:
            return True
        return False


class DirectInstruction(Instruction):
    def apply(self, item):
        return self.res


class RequiredState:
    def __init__(self):
        self.min_values = {
            'x': 1,
            'm': 1,
            'a': 1,
            's': 1,
        }
        self.max_values = {
            'x': 4000,
            'm': 4000,
            'a': 4000,
            's': 4000,
        }

    def __repr__(self):
        res = []
        for c in 'xmas':
            res.append(f"{str(self.min_values[c])} <= {c} <= {str(self.max_values[c])}")
        return f"<<<RequiredState {' '.join(res)}>>>"

    def add_req(self, kind: str, op, value, invert_this):
        if invert_this:
            op = '>' if op == '<' else '<'
        else:
            # change to strict equality
            value = value + (-1 if op == '<' else 1)
        if op == '<':
            self.max_values[kind] = min(self.max_values[kind], value)
        else:
            self.min_values[kind] = max(self.min_values[kind], value)

    def total_range_for(self, kind):
        return max(0, self.max_values[kind] - self.min_values[kind] + 1)

    def total_number_of(self):
        product = 1
        for c in 'xmas':
            product *= self.total_range_for(c)
        return product


class Solver:

    def __init__(self):
        with open('input.json', 'r', encoding='utf-8') as f:
            self.raw_data = json.load(f)
        self.workflows = self.parse_data()
        self.accepted = []

    def parse_data(self):
        workflows = {}
        for line in self.raw_data['workflows'].split('\n'):
            name = re.search(r'^(\w*)', line)[0]
            instr_raw = re.search(r'{(.*)}', line)[1]
            instr = []
            for ins in instr_raw.split(','):
                if re.search(r'^\w*$', ins):
                    instr.append(DirectInstruction(res=ins))
                else:
                    instr.append(Instruction(ins[0], ins[1],
                                             re.search(r'[<>](\d*):', ins)[1],
                                             re.search(r'(\w*)$', ins)[1]
                                             ))
            cur_item = {
                'raw': line,
                'name': name,
                'instr': instr,
            }
            workflows[name] = cur_item
        return workflows

    def run(self):
        self.bfs(RequiredState(), 'in')
        print(self.accepted)
        return sum(x.total_number_of() for x in self.accepted)

    def bfs(self, cur_state: RequiredState, next_rule: str):
        if next_rule == 'R':
            return
        if next_rule == 'A':
            self.accepted.append(cur_state)
            # print(cur_state)
            return
        next_instruction_set = self.workflows[next_rule]['instr']
        # print(next_rule, next_instruction_set)
        for instr in next_instruction_set:
            # print('cur state for rule', next_rule, cur_state)
            next_state = deepcopy(cur_state)
            if instr.kind != '':
                next_state.add_req(instr.kind, instr.op, instr.limit, False)
            self.bfs(next_state, instr.res)
            cur_state = deepcopy(cur_state)
            if instr.kind == '':
                continue
            cur_state.add_req(instr.kind, instr.op, instr.limit, True)


if __name__ == '__main__':
    print(Solver().run())
