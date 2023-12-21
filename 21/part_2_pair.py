import numpy as np

inp = open('input.txt').read().strip()

steps = 26501365

walls = np.array([[True if char != '#' else False for char in line] for line in inp.split('\n')])
available_squares = np.array([[True if char == 'S' else False for char in line] for line in inp.split('\n')])
old = np.zeros(available_squares.shape)

# do a flood fill to make sure we don't count any totally-surrounded `.`s in our solution
while not np.array_equal(old, available_squares):
    old = available_squares
    next_available_squares = available_squares.copy()
    for x in range(len(available_squares)):
        for y in range(len(available_squares[0])):
            if available_squares[x, y]:
                for xo in (-1, 0, 1):
                    for yo in (-1, 0, 1):
                        if 0 not in (xo, yo) or xo == yo == 0 \
                                or not (0 <= x + xo < len(available_squares)) \
                                or not (0 <= y + yo < len(available_squares[0])):
                            continue
                        next_available_squares[x + xo][y + yo] = True
    next_available_squares &= walls
    available_squares = next_available_squares

enclosure_order = (steps - (len(available_squares) // 2)) // len(available_squares)
print('o', enclosure_order)
odd_parity_mask = np.array(
    [[(x + y) % 2 == 0 for y in range(len(available_squares[0]))] for x in range(len(available_squares))])
tl_triangle_mask = np.array(
    [[(x + y) < (len(available_squares) // 2) for y in range(len(available_squares[0]))] for x in
     range(len(available_squares))])

inv = np.vectorize(lambda v: not v)


def repr_mask(mask):
    return '\n'.join(''.join('#' if val else '.' for val in line) for line in mask)


# avoid overflow error by doing each one individually, then put into wolfram|alpha
totals = []

# Tips
tip_mask = inv(odd_parity_mask) & inv(tl_triangle_mask) & np.rot90(inv(tl_triangle_mask))
for rot in range(4):
    totals.append((available_squares & tip_mask).sum())
    tip_mask = np.rot90(tip_mask)

# Chunks
tri_mask = tl_triangle_mask.copy()
for rot in range(4):
    totals.append((available_squares & odd_parity_mask & tri_mask).sum() * enclosure_order)
    totals.append((available_squares & inv(odd_parity_mask) & inv(tri_mask)).sum() * (enclosure_order - 1))
    tri_mask = np.rot90(tri_mask)

totals.append((available_squares & odd_parity_mask).sum() * enclosure_order ** 2)
totals.append((available_squares & inv(odd_parity_mask)).sum() * (enclosure_order - 1) ** 2)

print(totals)
