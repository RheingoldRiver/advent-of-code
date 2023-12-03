class Solver:
    str_to_digit = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9
    }

    def __init__(self):
        with open('input.txt', 'r', encoding='utf-8') as f:
            self.lines = f.readlines()

    def run(self):
        total = 0
        for line in self.lines:
            first_digit = None
            cur_digit = None
            for i, char in enumerate(line.strip()):
                digit = self.digit_at_pos(i, char, line)
                if digit is not None:
                    if cur_digit is None:
                        first_digit = digit
                    cur_digit = digit
            if cur_digit is not None:
                val = 10 * first_digit + cur_digit
                total += val
        return total

    def digit_at_pos(self, i: int, char: str, line: str):
        try:
            return int(char)
        except ValueError:
            pass
        for k, v in self.str_to_digit.items():
            if line[i:].startswith(k):
                return v
        return None

if __name__ == '__main__':
    print(Solver().run())