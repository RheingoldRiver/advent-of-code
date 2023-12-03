import re


class Solver:

    def __init__(self):
        with open('input.txt', 'r', encoding='utf-8') as f:
            self.lines = f.readlines()

    def run(self):
        total = 0
        for i, line in enumerate(self.lines):
            stripped_line = line.strip()
            for j, char in enumerate(stripped_line):
                # ignore this?
                if not self.is_number(char):
                    continue

                # did we already process this number?
                if j > 0 and self.is_number(stripped_line[j - 1]):
                    continue

                cur_num_string = re.match(r'^\d*', stripped_line[j:])[0]
                is_valid = False
                for k in range(len(cur_num_string)):
                    if self.symbol_next_to_square(i, j + k):
                        is_valid = True
                        break
                if is_valid:
                    total += int(cur_num_string)

        return total

    def symbol_next_to_square(self, i, j):
        max_i = len(self.lines) - 1
        max_j = len(self.lines[0]) - 1
        # vertical squares
        if i > 0 and self.is_symbol(self.lines[i - 1][j]):
            return True
        if i < max_i and self.is_symbol(self.lines[i + 1][j]):
            return True

        # horizontal squares
        if j > 0 and self.is_symbol(self.lines[i][j - 1]):
            return True
        if j < max_j and self.is_symbol(self.lines[i][j + 1]):
            return True

        # diagonal squares
        if j > 0 and i > 0 and self.is_symbol(self.lines[i - 1][j - 1]):
            return True
        if j < max_j and i < max_i and self.is_symbol(self.lines[i + 1][j + 1]):
            return True
        if i < max_i and j > 0 and self.is_symbol(self.lines[i + 1][j - 1]):
            return True
        if j < max_j and i > 0 and self.is_symbol(self.lines[i - 1][j + 1]):
            return True
        return False

    @staticmethod
    def is_symbol(char: str) -> bool:
        return re.match(r'[\d\\.\s]', char) is None

    @staticmethod
    def is_number(char: str) -> bool:
        return re.match(r'\d', char) is not None


if __name__ == '__main__':
    print(Solver().run())
