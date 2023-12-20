import string
from typing import List, Dict

COUNT_HIGH_PULSES = 0
COUNT_LOW_PULSES = 0
ALL_NODES: Dict[str, "Node"] = {}


class Signal:
    logging = False

    def __init__(self, pulse_type: str, source: "Node", target: "Node"):
        self.pulse_type = pulse_type
        self.source = source
        self.target = target

    def log(self):
        if self.logging:
            print(f'{self.source.name} -{self.pulse_type}-> {self.target.name}')


queue: List[Signal] = []


def send_pulse(signal: Signal):
    global COUNT_HIGH_PULSES
    global COUNT_LOW_PULSES
    if signal.pulse_type == 'HIGH':
        COUNT_HIGH_PULSES += 1
    else:
        COUNT_LOW_PULSES += 1
    queue.append(signal)


class Node:
    FLIP_FLOP = '%'
    BROADCASTER = 'broadcaster'
    CONJUNCTION = '&'
    node_type = 'None'

    def __repr__(self):
        return f"<FlipFlopNode {self.name} -> [{', '.join(self.outputs)}]>"

    def __init__(self, name):
        self.name = name
        self.outputs = []

    def add_output(self, output: str):
        self.outputs.append(output)

    def send_pulse(self, pulse_type, prev_node: "Node"):
        global ALL_NODES
        for node in self.outputs:
            send_pulse(Signal('LOW', self, ALL_NODES[node]))


class FlipFlopNode(Node):
    node_type = 'FlipFlop'

    def __repr__(self):
        return f"<FlipFlopNode {self.name} -> [{', '.join(self.outputs)}]>"

    def __init__(self, name):
        super().__init__(name)
        self.status = 0

    def send_pulse(self, pulse_type, prev_node: Node):
        global COUNT_HIGH_PULSES
        global COUNT_LOW_PULSES
        global ALL_NODES
        if pulse_type == 'HIGH':
            return
        if self.status == 0:
            self.status = 1
            for node in self.outputs:
                send_pulse(Signal('HIGH', self, ALL_NODES[node]))
        else:
            self.status = 0
            for node in self.outputs:
                send_pulse(Signal('LOW', self, ALL_NODES[node]))


class ConjunctionNode(Node):
    node_type = 'Conjunction'

    def __repr__(self):
        return f"<FlipFlopNode {self.name} -> [{', '.join(self.outputs)}]>"

    def __init__(self, name):
        super().__init__(name)
        self.statuses = {}

    def add_input(self, name):
        self.statuses[name] = 'LOW'

    @property
    def status(self):
        return 'HIGH' if all([x == 'HIGH' for x in self.statuses.values()]) else 'LOW'

    def send_pulse(self, pulse_type, prev_node: Node):
        global COUNT_HIGH_PULSES
        global COUNT_LOW_PULSES
        global ALL_NODES
        self.update_status(pulse_type, prev_node)
        if self.status == 'HIGH':
            for node in self.outputs:
                send_pulse(Signal('LOW', self, ALL_NODES[node]))
        else:
            for node in self.outputs:
                send_pulse(Signal('HIGH', self, ALL_NODES[node]))

    def update_status(self, pulse_type, prev_node):
        self.statuses[prev_node.name] = pulse_type


class EndpointNode(Node):
    def __init__(self, name):
        super().__init__(name)

    def __repr__(self):
        return f"<EndpointNode {self.name}>"

    def send_pulse(self, pulse_type, prev_node: Node):
        pass


class Solver:

    def __init__(self):
        with open('input.txt', 'r', encoding='utf-8') as f:
            self.lines = [line.strip() for line in f.readlines()]
        for line in self.lines:
            self.parse_line(line)
        to_add = {}
        for name, node in ALL_NODES.items():
            for o in node.outputs:
                if o not in ALL_NODES.keys() and o not in to_add.keys():
                    to_add[o] = EndpointNode(o)
            if node.node_type != ConjunctionNode.node_type:
                continue
            node: ConjunctionNode
            for k, v in ALL_NODES.items():
                if name in v.outputs:
                    print(k, ' -> ', v)
                    node.add_input(k)
        ALL_NODES.update(to_add)
        print(ALL_NODES)

    def parse_line(self, line):
        info, outputs = line.split(' -> ')
        node = None
        if info[0] in string.ascii_lowercase:
            node = Node(info)
        elif info[0] == Node.FLIP_FLOP:
            node = FlipFlopNode(info[1:])
        elif info[0] == Node.CONJUNCTION:
            node = ConjunctionNode(info[1:])
        else:
            raise ValueError(info)
        for output in outputs.split(','):
            node.add_output(output.strip())
        ALL_NODES[node.name] = node

    def run(self):
        global queue
        global ALL_NODES
        count = 0
        should_break = False
        found_jg = False
        found_rh = False
        found_jm = False
        found_hf = False
        while True:
            count += 1
            send_pulse(Signal('LOW', Node('broadcaster'),
                              ALL_NODES['broadcaster']))  # source doesnt matter here only the target
            while len(queue) > 0:
                next_signal = queue.pop(0)
                next_signal.log()
                next_signal.target.send_pulse(next_signal.pulse_type, next_signal.source)
                if not found_jg and next_signal.source.name == 'jg' and next_signal.pulse_type == 'HIGH':
                    print('jg ', count)
                    found_jg = True
                if not found_rh and next_signal.source.name == 'rh' and next_signal.pulse_type == 'HIGH':
                    print('rh ', count)
                    found_rh = True
                if not found_jm and next_signal.source.name == 'jm' and next_signal.pulse_type == 'HIGH':
                    print('jm ', count)
                    found_jm = True
                if not found_hf and next_signal.source.name == 'hf' and next_signal.pulse_type == 'HIGH':
                    print('hf ', count)
                    found_hf = True
            if found_hf and found_jm and found_jg and found_rh:
                break


if __name__ == '__main__':
    print(Solver().run())
