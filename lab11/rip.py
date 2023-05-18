#!/usr/bin/env python
import json
from random import randint
from rich.console import Console
from rich.table import Table

console = Console()


def generate_ip():
    a = [str(randint(1, 255)) if i == 0 else str(randint(0, 255))
         for i in range(4)]
    return '.'.join(a)


def generate_network(path, count=5, connection_proba=0.2):
    structure = {generate_ip(): {} for _ in range(count)}
    for ip in structure:
        for ip_dest in structure:
            if ip == ip_dest:
                continue
            if ip_dest in structure[ip].keys():
                continue
            if randint(1, count * 10) <= connection_proba * 100 / 2:
                structure[ip][ip_dest] = [ip_dest, 1]
                structure[ip_dest][ip] = [ip, 1]

    json_object = json.dumps(structure, indent=4)
    with open(path, 'w') as f:
        f.write(json_object)


def load_network(path):
    with open(path, 'r') as f:
        network = json.load(f)
    return network


def print_network(network):
    table = Table(title='Starting table of connections')
    head = ['Source IP', 'Connections']
    for c in head:
        table.add_column(c)

    for node in network:
        table.add_row(node, ', '.join(
            [network[node][node_dest][0] for node_dest in network[node]]))

    console.print(table)


def print_table(node, network, title=''):
    table = Table(title=title)
    head = ['Source IP', 'Destination IP', 'Next Hop', 'Metric']
    for c in head:
        table.add_column(c)

    for node_dest in network[node]:
        table.add_row(node, node_dest, network[node][node_dest][0], str(
            network[node][node_dest][1]))

    console.print(table)


def rip(network, verbose=False):
    for i in range(1, len(network)):
        stagnant = True
        for node_dest in network:
            for node_src in network[node_dest]:
                if network[node_dest][node_src][1] != 1:  # traverse only by direct routes
                    continue
                for connection in network[node_dest]:
                    if connection == node_src:
                        continue
                    if connection not in network[node_src] \
                            or network[node_dest][connection][1] + 1 < network[node_src][connection][1]:
                        network[node_src][connection] = (node_dest,
                                                         network[node_dest][connection][1] + 1)
                        stagnant = False

        if stagnant:
            break

        if verbose:
            for node in network:
                print_table(node, network,
                            title=f'Simulation step {i} of router {node}')
    return network


if __name__ == '__main__':
    generate_network('schema.json')
    net = load_network('schema.json')
    print_network(net)

    net = rip(net, verbose=True)
    for n in net:
        print_table(n, net, title=f'Final state of router {n} table')
