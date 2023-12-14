from copy import copy

from utils.grid.grid import Grid


class Solver:

    def __init__(self):
        with open('input.txt', 'r', encoding='utf-8') as f:
            self.raw_data = f.read()
        self.data = self.parse_data()

    def parse_data(self):
        grids = [Grid.read_from_lines(grid.split('\n')) for grid in self.raw_data.split('\n\n')]
        return grids

    def run(self):
        total = 0
        product = 1
        for grid in self.data:
            if (col := self.reflection_over_col(grid)) is not None:
                total += col
            elif (row := self.reflection_over_row(grid)) is not None:
                total += 100 * row
        return total

    def reflection_over_row(self, grid: Grid):
        valid_cols = []
        i = 0
        for col in grid.all_columns(False):
            valid_cols.append(self.get_allowed_positions(col))
            i += 1
        solutions = self.intersection(valid_cols)
        if len(solutions) > 0:
            return solutions.pop()
        print('over row')
        print(valid_cols)
        print(solutions)
        return None

    def reflection_over_col(self, grid: Grid):
        valid_rows = []
        i = 0
        for row in grid.all_rows(False):
            valid_rows.append(self.get_allowed_positions(row))
            i += 1
        solutions = self.intersection(valid_rows)
        print(valid_rows)
        if len(solutions) > 0:
            return solutions.pop()
        print('over col')
        print(valid_rows)
        print(solutions)
        return None

    @staticmethod
    def row_as_string(row):
        return ''.join(str(cell) for cell in row)

    def get_allowed_positions(self, row):

        valid = []
        # print(f'*************** starting processing {self.row_as_string(row)}')
        for i in range(1, len(row)):
            # print(f'i: {i}')
            first_array = copy(row[:i])
            first_array.reverse()
            first = self.row_as_string(first_array)
            second = self.row_as_string(row[i:])
            # print(f"{self.row_as_string(row)} {i} first: {first} second: {second}")
            if first.startswith(second) or second.startswith(first):
                # print(f'valid: {i}')
                valid.append(i)

            # if i is 3 then

            # is_valid = True
            # for k in range(min(i, len(row) - i)):
            #     j = k + 1
            #     print(f'j: {j}')
            #     # check 2 & 4
            #     # then check 1 & 5
            #     # then check 0 & 6
            #
            #     # but if len is 5 then we can only check 4, 5
            #     # len(row) - i = 2
            #     if row[i - j] != row[i + j]:
            #         is_valid = False
            #         break
            # if is_valid:
            #     valid.append(i)
        # print(valid)
        return valid

    @staticmethod
    def intersection(valid_items):
        common_items = set(valid_items[0])

        for sublist in valid_items[1:]:
            common_items = common_items.intersection(sublist)
        return common_items


if __name__ == '__main__':
    print(Solver().run())
