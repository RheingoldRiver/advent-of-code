import json
import re
from copy import copy, deepcopy
from typing import List


class Solver:
    cards = {
        'A': 14,
        'K': 13,
        'Q': 12,
        'J': 0,
        'T': 10,
        '9': 9,
        '8': 8,
        '7': 7,
        '6': 6,
        '5': 5,
        '4': 4,
        '3': 3,
        '2': 2,
    }

    def __init__(self):
        with open('input.txt', 'r', encoding='utf-8') as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.data = self.parse_lines()

    def parse_lines(self) -> List:
        data = []
        for line in self.lines:
            card = {
                'hand': line.split()[0],
                'bid': int(line.split()[1]),
            }
            card['unique'] = len(set(card['hand']))
            card['score'] = self.get_score(card)
            card['tiebreak_score'] = self.tiebreak_score(card['hand'])
            print(f"{card['hand']} {card['bid']} unique: {card['unique']} tiebreak: {card['tiebreak_score']} score: {card['score']}")
            data.append(card)
        return data

    def run(self):
        total = 0
        sorted_data = sorted(self.data, key=self.get_score)
        for i, line in enumerate(sorted_data):
            print(line['bid'])
            total += (i + 1) * line['bid']
        return total

    def power(self, n, value):
        return 10 ** (n * 2) * 1

    @staticmethod
    def dict_of_amount(hand):
        ret = {}
        for card in hand:
            if card in ret.keys():
                ret[card] += 1
            else:
                ret[card] = 1
        return ret

    def get_score(self, line):
        unsorted_hand = list(line['hand'])
        hand = sorted(list(line['hand']), key=lambda x: self.cards[x])
        hand.reverse()
        # hand is now in descending order
        num_unique_items = len(set(hand))
        dict_of_amount = self.dict_of_amount(hand)
        profile = dict_of_amount.values()
        tiebreak_score = self.tiebreak_score(unsorted_hand)
        print(profile)
        if self.match_profile(profile, [5]):
            return 10 ** 4 + tiebreak_score
        if self.match_profile(profile, [4, 1]):
            return 5 * 10 ** 3 + tiebreak_score
        if self.match_profile(profile, [3, 2]):
            return 10 ** 3 + tiebreak_score
        if self.match_profile(profile, [3, 1]):
            return 5 * 10 ** 2 + tiebreak_score
        if self.match_profile(profile, [2, 1]) and len(profile) == 3:
            return 10 ** 2 + tiebreak_score
        if self.match_profile(profile, [2, 1]) and len(profile) == 4:
            return 5 * 10 + tiebreak_score
        return 10 + tiebreak_score
        # if num_unique_items == 1:  # 5 of a kind
        #     return self.power(7, hand[0]) + self.tiebreak_score(unsorted_hand)
        # if num_unique_items == 2:  # 4 of a kind or full house
        #     if hand[1] == hand[3]:
        #         other_val = hand[0] if hand[4] == hand[1] else hand[4]
        #         return self.power(6, hand[1]) + self.tiebreak_score(unsorted_hand)
        #     else:
        #         # full house, so the 3rd card is the one with more
        #         other_val = hand[1] if hand[3] == hand[2] else hand[3]
        #         return self.power(5, hand[3]) + self.tiebreak_score(unsorted_hand)
        # if num_unique_items == 3:
        #     score = 0
        #     for card in hand:
        #         if dict_of_amount[card] == 3:
        #             score += self.power(4, card)
        #             break
        #         if dict_of_amount[card] == 2:
        #             score += self.power(3, card)
        #             break
        #     return score + self.tiebreak_score(unsorted_hand)
        # if num_unique_items == 4:
        #     score = 0
        #     for i, card in enumerate(hand):
        #         if dict_of_amount[card] == 2:
        #             score += self.power(1, card)
        #             break
        #         # else:
        #         #     score += self.power(-1 * i, card)
        #     return score + self.tiebreak_score(unsorted_hand)
        # if num_unique_items == 5:  # highest number
        #     return self.power(0, hand[0]) + self.tiebreak_score(unsorted_hand)

    def tiebreak_score(self, hand):
        score = 0
        for i, card in enumerate(hand):
            score += self.tiebreak_power(i, card)
        return score

    def tiebreak_power(self, n, value):
        return 10 ** ((n + 1) * -2) * self.cards[value]

    @staticmethod
    def match_profile(values, allowed):
        return all(x in allowed for x in values) and all(x in values for x in allowed)

if __name__ == '__main__':
    print(Solver().run())
