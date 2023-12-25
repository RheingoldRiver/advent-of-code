import networkx


class Solver:

    def __init__(self):
        with open('input.txt', 'r', encoding='utf-8') as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.data = [self.parse_line(i, line) for i, line in enumerate(self.lines)]
        self.graph = networkx.Graph()
        self.build_graph()

    def parse_line(self, i: int, line: str):
        name, children = line.split(': ')
        ret = {
            "name": name,
            "children": children.split(' ')
        }
        return ret

    def build_graph(self):
        for line in self.data:
            self.graph.add_node((line['name']))

        for line in self.data:
            for child in line['children']:
                self.graph.add_edge(line['name'], child)

    def run(self):
        total = 0
        for (a, b) in networkx.minimum_edge_cut(self.graph):
            self.graph.remove_edge(a, b)
        for c in networkx.connected_components(self.graph):
            print(len(c))

        return total


if __name__ == '__main__':
    print(Solver().run())
