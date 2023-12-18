import json
import math
import re
from copy import copy, deepcopy

from utils.grid.cell import Cell
from utils.grid.errors import MoveError
from utils.grid.grid import Grid
from utils.grid.pointer import Pointer


class Solver:
    starting_pos_actual = Cell(row=209, col=128)
    starting_pos_test = Cell(row=1, col=1)

    def __init__(self):
        with open('input.txt', 'r', encoding='utf-8') as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.data = [self.parse_line(line) for line in self.lines]

        # nums1 = []
        # nums2 = []
        for line in self.data:
            print(line['steps'])
            # if line['direction'] in 'UD':
            #     nums1.append(line['steps'])
            # else:
            #     nums2.append(line['steps'])
        # print(math.gcd(*nums1))
        # print(math.gcd(*nums2))

    def parse_line(self, line):
        direction, steps, color = line.split(' ')
        color = color.replace('#', '').replace('(', '').replace(')', '').upper()
        steps = int(color[:5], 16)
        last_digit = color[-1]
        if last_digit == '0':
            direction = 'R'
        if last_digit == '1':
            direction = 'D'
        if last_digit == '2':
            direction = 'L'
        if last_digit == '3':
            direction = 'U'
        print(steps, direction)
        return {
            'direction': direction,
            'steps': steps,
            'color': color,
        }

    def run(self):
        points_of_interest = [Cell(0, 0)]
        old_cell = points_of_interest[0]
        for i, line in enumerate(self.data):
            new_cell = None
            if line['direction'] == 'U':
                new_cell = Cell(old_cell.row - line['steps'], old_cell.col)
            elif line['direction'] == 'D':
                new_cell = Cell(old_cell.row + line['steps'], old_cell.col, {'orig_index': i})
            elif line['direction'] == 'L':
                new_cell = Cell(old_cell.row, old_cell.col - line['steps'], {'orig_index': i})
            elif line['direction'] == 'R':
                new_cell = Cell(old_cell.row, old_cell.col + line['steps'], {'orig_index': i})
            old_cell = new_cell
            points_of_interest.append(new_cell)

        total = 0
        perimeter = 0
        for i, point in enumerate(points_of_interest):
            j = (i + 1) % len(points_of_interest)
            next_point = points_of_interest[j]
            total += point.row * next_point.col - point.col * next_point.row
            perimeter += max(abs(point.row - next_point.row), abs(next_point.col - point.col))

        area = abs(total) / 2
        return area, perimeter, area + perimeter, area + perimeter / 2, area + perimeter / 2 + 1

        # segments = self.get_line_segments(points_of_interest)
        # return self.count_enclosed_area(segments)

    def get_line_segments(self, points):
        segments = []
        for i in range(len(points) - 1):
            p1, p2 = points[i], points[i + 1]
            if p1.row == p2.row:  # Horizontal segment
                segments.append(('H', p1.row, min(p1.col, p2.col), max(p1.col, p2.col)))
            else:  # Vertical segment
                segments.append(('V', min(p1.row, p2.row), max(p1.row, p2.row), p1.col))
        return segments

    def count_enclosed_area(self, segments):
        segments.sort(key=lambda x: (x[1], x[2]))  # Sort by primary coordinate

        enclosed_area = 0
        scan_line = -1
        inside_polygon = False

        for seg in segments:
            if seg[0] == 'H':  # Horizontal segment
                if seg[1] != scan_line:
                    scan_line = seg[1]
                    inside_polygon = False
                if inside_polygon:
                    enclosed_area += seg[3] - seg[2] + 1
                inside_polygon = not inside_polygon
            else:  # Vertical segment
                if seg[1] > scan_line:
                    scan_line = seg[1]
                    inside_polygon = False

        return enclosed_area


if __name__ == '__main__':
    print(Solver().run())
