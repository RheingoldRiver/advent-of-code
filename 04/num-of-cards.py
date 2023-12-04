import re
from typing import List


class Solver:

    def __init__(self):
        with open('input.txt', 'r', encoding='utf-8') as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.data = self.parse_lines()

    def parse_lines(self):
        data = []
        for line in self.lines:
            split1 = line.split(':')
            card = int(split1[0].replace('Card ', '').strip())
            split2 = split1[1].split('|')
            winning_numbers_str = split2[0]
            picked_numbers_str = split2[1]
            winning_numbers = [int(_) for _ in winning_numbers_str.split()]
            picked_numbers = [int(_) for _ in picked_numbers_str.split()]
            data.append({
                'card': card,
                'winning_numbers': winning_numbers,
                'picked_numbers': picked_numbers,
            })
        return data

    def run(self):
        total = 0
        queue: List[int] = list(range(len(self.data)))
        queue.reverse()
        total_scores = {}
        for n in queue:
            num_points = 1 # for itself
            num_won = 0
            item = self.data[n]
            # compute score for this card
            for num in item['picked_numbers']:
                if num in item['winning_numbers']:
                    num_won += 1

            # compute remaining scores
            for i in range(n + 1, n + num_won + 1):
                if i < len(self.data):
                    num_points += total_scores[i]
            # caching or something
            total_scores[n] = num_points
            total += num_points

        return total


if __name__ == '__main__':
    print(Solver().run())
