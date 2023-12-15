import json
import re
from copy import copy, deepcopy


class Solver:

    def __init__(self):
        with open('input.txt', 'r', encoding='utf-8') as f:
            self.raw_input = [line.strip() for line in f.readlines()]
        self.data = self.raw_input[0].split(',')
        self.boxes = {}
        for i in range(256):
            self.boxes[i] = {
                'lenses': [],
                'labels': [],
            }

    def run(self):
        total = 0
        for step in self.data:
            print(f"{step}")
            operation = 'equals' if '=' in step else 'minus'
            if operation == 'minus':
                self.do_minus(step)
            else:
                self.do_equals(step)
            self.print_boxes(operation)

        for b, box in self.boxes.items():
            for i, lens in enumerate(box['lenses']):
                total += (lens * (len(box['lenses'])-i) * (b + 1))
        return total

    def print_boxes(self, operation):
        for i, box in self.boxes.items():
            if len(box['labels']) > 0:
                print(f"{i} {','.join(box['labels'])} {','.join([str(x) for x in box['lenses']])} - {operation}")

    def do_minus(self, step):
        label = step.split('-')[0]
        hash = self.get_hash(label)
        box = self.boxes[hash]
        if label in box['labels']:
            index = box['labels'].index(label)
            box['labels'].pop(index)
            box['lenses'].pop(index)

    def do_equals(self, step):
        label, lens = step.split('=')
        lens = int(lens)
        hash = self.get_hash(label)
        box = self.boxes[hash]
        if label in box['labels']:
            i = box['labels'].index(label)
            box['lenses'][i] = lens
        else:
            box['labels'].insert(0, label)
            box['lenses'].insert(0, lens)

    def get_hash(self, step):
        cur_value = 0
        for char in step:
            cur_value += ord(char)
            cur_value *= 17
            cur_value = cur_value % 256
        return cur_value


if __name__ == '__main__':
    print(Solver().run())
