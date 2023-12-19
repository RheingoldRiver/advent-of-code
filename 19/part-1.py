import json
import re
from copy import copy, deepcopy
from utils.grid.errors import MoveError
from utils.grid.grid import Grid
from utils.grid.pointer import Pointer

class Item:
    def __init__(self, x, m, a, s):
        self.x = int(x)
        self.m = int(m)
        self.a = int(a)
        self.s = int(s)

    def __repr__(self):
        return f"<Item x {self.x} m {self.m} a {self.a} s {self.s}>"

    def get(self, kind):
        if kind == 'x':
            return self.x
        elif kind == 'm':
            return self.m
        elif kind == 'a':
            return self.a
        elif kind == 's':
            return self.s

    def total(self):
        return self.x + self.m + self.a + self.s


class Instruction:
    noop = "PASS_THROUGH"
    accept = 'ACCEPT'
    reject = "REJECT"

    def __init__(self, kind: str = '', op: str = '', limit: str = '0', res: str = ''):
        self.kind = kind
        self._op = op
        self.limit = int(limit)
        self.res = res

    def __repr__(self):
        return f"<Instruction {self.kind} {self._op} {self.limit} -> {self.res}>"

    def apply(self, item: Item):
        if self.op(item.get(self.kind), self.limit):
            return self.res
        else:
            return self.noop

    def op(self, item: int, limit: int):
        if self._op == '<' and item < limit:
            return True
        if self._op == '>' and item > limit:
            return True
        return False


class DirectInstruction(Instruction):
    def apply(self, item):
        return self.res

# class RejectInstruction(Instruction):
#     def apply(self, item):
#         return self.reject
#
# class AcceptInstruction(Instruction):
#     def apply(self, item):
#         return self.accept


class Solver:

    def __init__(self):
        with open('input.json', 'r', encoding='utf-8') as f:
            self.raw_data = json.load(f)
        self.workflows, self.items = self.parse_data()

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
        ratings = []
        for item in self.raw_data['ratings'].split('\n'):
            for i in 'xmas':
                item = item.replace(i, f'"{i}"')
            item = item.replace('=', ':')
            j = json.loads(item)
            ratings.append(Item(j['x'], j['m'], j['a'], j['s']))
        return workflows, ratings

    def run(self):
        total = 0
        accepted = []
        rejected = []
        for item in self.items:
            cur_workflow = self.workflows['in']
            result = False
            while True:
                print(cur_workflow)
                for instruction in cur_workflow['instr']:
                    res = instruction.apply(item)
                    if res == Instruction.noop:
                        continue
                    if res == 'R':
                        rejected.append(item)
                        result = True
                        break
                    if res == 'A':
                        accepted.append(item)
                        result = True
                        break
                    cur_workflow = self.workflows[res]
                    break
                if result:
                    break
        print(accepted)
        print(rejected)
        print([item.total() for item in accepted])
        return sum([item.total() for item in accepted])


if __name__ == '__main__':
    print(Solver().run())
