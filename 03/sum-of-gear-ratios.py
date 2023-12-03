import re
from typing import List, Union


class Solver:

    def __init__(self):
        with open('input.txt', 'r', encoding='utf-8') as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.data = self.transform()

    def transform(self) -> List[List[Union[str, int]]]:
        data = []
        idx = 0
        for line in self.lines:
            transformed_line = []
            for j, char in enumerate(line):
                if len(transformed_line) > j:
                    continue
                if self.is_digit(char):
                    num = re.match(r'^\d*', line[j:])[0]
                    for k in range(len(num)):
                        transformed_line.append({
                            'num': int(num),
                            'idx': idx,
                        })
                    idx += 1
                else:
                    transformed_line.append(char)
            data.append(transformed_line)
        return data

    def run(self):
        total = 0
        for i, line in enumerate(self.data):
            for j, char in enumerate(line):
                # ignore this?
                if type(char) is not str:
                    continue
                if not self.is_symbol(char):
                    continue

                adjacent_numbers = self.get_adjacent_numbers(i, j)
                if len(adjacent_numbers) == 2:
                    total += adjacent_numbers[0] * adjacent_numbers[1]

        return total

    def get_adjacent_numbers(self, i, j) -> List[int]:
        max_i = len(self.data) - 1
        max_j = len(self.data[0]) - 1
        adjacent_numbers = []
        found_ids = []
        # vertical squares
        if i > 0 and self.is_number(pos := self.data[i - 1][j]):
            self.append_if_valid(pos, adjacent_numbers, found_ids)
        if i < max_i and self.is_number(pos := self.data[i + 1][j]):
            self.append_if_valid(pos, adjacent_numbers, found_ids)

        # horizontal squares
        if j > 0 and self.is_number(pos := self.data[i][j - 1]):
            self.append_if_valid(pos, adjacent_numbers, found_ids)
        if j < max_j and self.is_number(pos := self.data[i][j + 1]):
            self.append_if_valid(pos, adjacent_numbers, found_ids)

        # diagonal squares
        if j > 0 and i > 0 and self.is_number(pos := self.data[i - 1][j - 1]):
            self.append_if_valid(pos, adjacent_numbers, found_ids)
        if j < max_j and i < max_i and self.is_number(pos := self.data[i + 1][j + 1]):
            self.append_if_valid(pos, adjacent_numbers, found_ids)
        if i < max_i and j > 0 and self.is_number(pos := self.data[i + 1][j - 1]):
            self.append_if_valid(pos, adjacent_numbers, found_ids)
        if j < max_j and i > 0 and self.is_number(pos := self.data[i - 1][j + 1]):
            self.append_if_valid(pos, adjacent_numbers, found_ids)
        return adjacent_numbers

    @staticmethod
    def append_if_valid(char, adjacent_numbers: List[int], found_ids: List[int]):
        if char['idx'] in found_ids:
            return
        adjacent_numbers.append(char['num'])
        found_ids.append(char['idx'])

    @staticmethod
    def is_symbol(char: str) -> bool:
        return re.match(r'[\d\\.\s]', char) is None

    @staticmethod
    def is_digit(char: str) -> bool:
        return re.match(r'\d', char) is not None

    @staticmethod
    def is_number(char: str) -> bool:
        return type(char) is not str


if __name__ == '__main__':
    print(Solver().run())
