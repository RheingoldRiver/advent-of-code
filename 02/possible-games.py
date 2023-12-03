import re


class Solver:
    max_allowed = {
        'red': 12,
        'green': 13,
        'blue': 14,
    }

    def __init__(self):
        with open('games.txt', 'r', encoding='utf-8') as f:
            self.lines = f.readlines()

    def run(self):
        total = 0
        for line in self.lines:
            valid = True
            for color, max_amt in self.max_allowed.items():
                for num in re.findall(f'(\d+) {color}', line):
                    if int(num) > max_amt:
                        valid = False
            if valid:
                total += int(re.search('Game (\d+)', line)[1])
        return total

if __name__ == '__main__':
    print(Solver().run())