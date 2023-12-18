import networkx
import numpy as np

# writeen by Aradia when we pair programmed this problem

inp = open('input.txt').read().strip()

grid = np.array([[int(val) for val in line] for line in inp.split('\n')])

#  right, left, down, up
dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

graph = networkx.DiGraph()

for x in range(len(grid)):
    for y in range(len(grid[0])):
        for possible_dir in dirs:
            for count in range(1, 11):
                graph.add_node((x, y, possible_dir, count))

for x, y, possible_dir, count in graph.nodes:
    if count < 4:
        legal_dirs = [possible_dir] if (0 <= x + possible_dir[0] < len(grid)) and (0 <= y + possible_dir[1] < len(grid[0])) else []
    else:
        legal_dirs = [ndir for ndir in dirs if ndir != (-possible_dir[0], -possible_dir[1])]
        legal_dirs = [ndir for ndir in legal_dirs
                      if (0 <= x + ndir[0] < len(grid))
                      and (0 <= y + ndir[1] < len(grid[0]))]
        if count == 10 and possible_dir in legal_dirs:
            legal_dirs.remove(possible_dir)
    for ndir in legal_dirs:
        graph.add_edge((x, y, possible_dir, count),
                       (x + ndir[0], y + ndir[1], ndir, 1 if ndir != possible_dir else count + 1),
                       weight=grid[x + ndir[0], y + ndir[1]])

start = (0, 0, None, 0)
graph.add_node(start)
graph.add_edge(start, (1, 0, (1, 0), 1), weight=grid[1, 0])
graph.add_edge(start, (0, 1, (0, 1), 1), weight=grid[0, 1])


def calc_path(path):
    last = path.pop(0)
    dist = 0
    for node in path:
        dist += graph.edges[last, node]['weight']
        last = node
    return dist


endpos = (len(grid) - 1, len(grid[0]) - 1)
best = 9999999999
for possible_dir in dirs:
    for count in range(4, 11):
        print(possible_dir, count)
        try:
            path = networkx.dijkstra_path(graph, start, (*endpos, possible_dir, count))
            best = min(best, calc_path(path))
        except networkx.exception.NetworkXNoPath:
            pass

        # print(calc_path(path))
        # print(path)
        # show = np.zeros(grid.shape, dtype=int)
        # for x, y, _, _ in path:
        #     show[x,y] = 1
        # print('\n'.join(''.join(map(str, line)) for line in show))
print(best)
