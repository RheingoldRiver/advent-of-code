import json
import math


class Solver:
    start = 'AAA'
    end = 'ZZZ'

    def __init__(self):
        with open('info.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        self.directions = self.data["line1"] * 2000000
        self.resulting_options = [self.parse_line(line) for line in self.data["lookup"].split('\n')]
        self.lookup = {item['start']: item for item in self.resulting_options}

    @staticmethod
    def parse_line(line):
        start = line.split(' = ')[0]
        results = line.split(' = ')[1].replace('(', '').replace(')', '')
        return {
            'start': start,
            'L': results.split(', ')[0],
            'R': results.split(', ')[1],
        }

    def run(self):
        total = 0
        cur = [loc for loc in self.lookup.keys() if loc.endswith('A')]
        prime_factors = [None] * len(cur)
        for char in self.directions:
            total += 1
            for i, loc in enumerate(cur):
                new_square = self.lookup[loc][char]
                cur[i] = new_square
                if new_square.endswith('Z') and prime_factors[i] is None:
                    prime_factors[i] = total
            print(prime_factors)
            if all(x is not None for x in prime_factors):
                break
        print(prime_factors)

        return math.lcm(*prime_factors)


if __name__ == '__main__':
    print(Solver().run())
