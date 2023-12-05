import json
from copy import copy


class Solver:

    def __init__(self):
        with open('info.json', 'r', encoding='utf-8') as f:
            self.raw_data = json.load(f)
        self.data = self.parse_lines()

    def parse_lines(self):
        data = {
            'seeds': [int(x) for x in self.raw_data['seeds'].split()],
            'maps': [self.parse_map(x) for x in self.raw_data['maps']]
        }
        return data

    @classmethod
    def parse_map(cls, map_set):
        return [cls.parse_one_entry(x) for x in map_set.split('\n')]

    @staticmethod
    def parse_one_entry(entry):
        destination = int(entry.split()[0])
        source = int(entry.split()[1])
        length = int(entry.split()[2])
        return {
            'destination': destination,
            'source': source,
            'length': length,
            'difference': destination - source,
            'min': source,
            'max': source + length,
        }

    def run(self):
        seeds = copy(self.data['seeds'])
        for seed_map in self.data['maps']:
            seeds = [self.do_map(seed, seed_map) for seed in seeds]
        return min(seeds)

    @staticmethod
    def do_map(n, seed_map):
        for map_item in seed_map:
            if map_item['max'] > n >= map_item['min']:
                return n + map_item['difference']
        return n


if __name__ == '__main__':
    print(Solver().run())
