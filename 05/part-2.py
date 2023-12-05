import json
from copy import deepcopy


class Solver:

    def __init__(self):
        with open('info.json', 'r', encoding='utf-8') as f:
            self.raw_data = json.load(f)
        self.data = self.parse_lines()

    def parse_lines(self):
        data = {
            'seeds': [self.parse_seed(x) for x in self.raw_data['seeds'].split(';')],
            'maps': [self.parse_map(x) for x in self.raw_data['maps']]
        }
        return data

    @staticmethod
    def parse_seed(seed):
        start = int(seed.split()[0])
        length = int(seed.split()[1])
        return {
            'min': start,
            'max': start + length - 1
        }

    @classmethod
    def parse_map(cls, map_set):
        return [cls.parse_one_entry(x) for x in map_set.split('\n')]

    @staticmethod
    def parse_one_entry(entry):
        destination = int(entry.split()[0])
        source = int(entry.split()[1])
        length = int(entry.split()[2])
        return {
            'difference': destination - source,
            'min': source,
            'max': source + length - 1,
        }

    def run(self):
        seeds = deepcopy(self.data['seeds'])
        for seed_map in self.data['maps']:
            found_this_round = []
            not_found_yet = []
            for map_item in seed_map:
                not_found_yet = []
                print(f'about to process: {str(seeds)}')
                for seed in seeds:
                    if map_item['max'] < seed['min']:
                        print(f'case 1 - {str(seed)}')
                        not_found_yet.append(seed)
                        continue
                    if map_item['min'] > seed['max']:
                        print(f'case 2 - {str(seed)}')
                        not_found_yet.append(seed)
                        continue
                    if map_item['min'] <= seed['min'] and map_item['max'] >= seed['max']:
                        # map contains the entire seed round; we dont need to look anymore
                        print(f'case 3 - {str(seed)}')
                        found_this_round.append({
                            'min': seed['min'] + map_item['difference'],
                            'max': seed['max'] + map_item['difference'],
                        })
                        continue
                    if seed['min'] < map_item['min'] <= seed['max'] <= map_item['max']:
                        # the map item min is between seed min and seed max
                        print(f'case 4 - {str(seed)}')
                        # what we didnt find
                        not_found_yet.append({
                            'min': seed['min'],
                            'max': map_item['min'] - 1
                        })
                        # what we found
                        found_this_round.append({
                            'min': map_item['min'] + map_item['difference'],
                            'max': seed['max'] + map_item['difference']
                        })
                    if map_item['min'] <= seed['min'] <= map_item['max'] < seed['max']:
                        print(f'case 5 - {str(seed)}')
                        found_this_round.append({
                            'min': seed['min'] + map_item['difference'],
                            'max': map_item['max'] + map_item['difference']
                        })
                        not_found_yet.append({
                            'min': map_item['max'] + 1,
                            'max': seed['max']
                        })
                    if map_item['min'] > seed['min'] and map_item['max'] < seed['max']:
                        print(f'case 6 - {str(seed)}')
                        found_this_round.append({
                            'min': map_item['min'] + map_item['difference'],
                            'max': map_item['max'] + map_item['difference'],
                        })
                        not_found_yet.append({
                            'min': seed['min'],
                            'max': map_item['min'] - 1,
                        })
                        not_found_yet.append({
                            'min': map_item['max'] + 1,
                            'max': seed['max'],
                        })
                seeds = not_found_yet
                print(f"one map range: {str(seeds)} ({map_item['min']} -> {map_item['max']})")
            seeds = found_this_round + not_found_yet
            print(f"new entire round**************: {str(seeds)}")

        return min([seed['min'] for seed in seeds])

    @staticmethod
    def do_map(n, seed_map):
        for map_item in seed_map:
            if map_item['max'] > n >= map_item['min']:
                return n + map_item['difference']
        return n


if __name__ == '__main__':
    print(Solver().run())
