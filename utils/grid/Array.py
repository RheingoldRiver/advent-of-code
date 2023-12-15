from typing import List

from utils.grid.cell import Cell


class Array:
    def __init__(self, array: List[Cell]):
        self.array = array

    def __repr__(self):
        return f"<Array object with length {len(self)}>"

    def __len__(self):
        return len(self.array)

    def __str__(self):
        return ''.join([str(x) for x in self.array])

    def __iter__(self):
        return iter(self.array)

    def __getitem__(self, key):
        return self.array[key]

    @property
    def max_val(self):
        return len(self) - 1

    def reversed(self):
        for i in range(len(self)):
            yield self.array[self.max_val - i]

    @property
    def min_index(self):
        return 0

    def all_possible_splits(self, num_pieces: int = 2, min_size: int = 1):
        def _generate_splits(array, partition_so_far, num_pieces_left):
            if num_pieces_left == 1:
                if len(array) >= min_size:
                    yield partition_so_far + (array,)
                return
            for i in range(min_size, len(array) - (num_pieces_left - 1) * min_size + 1):
                for split in _generate_splits(array[i:], partition_so_far + (array[:i],), num_pieces_left - 1):
                    yield split

        return _generate_splits(self.array, tuple(), num_pieces)

    def string_and_split(self, char):
        return str(self).split(char)

    def total_weight(self):
        return sum([x.weight for x in self.array])

    def overwrite_values(self, new_values):
        if len(new_values) != len(self):
            raise ValueError
        for i, x in enumerate(new_values):
            self.array[i].set_value(x)
