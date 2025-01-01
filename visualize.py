#! /usr/bin/python3

import subprocess
import os
import networkx as nx
import itertools
import matplotlib.pyplot as plt
import matplotlib as mpl
from progress.bar import Bar

CHECKER_PATH = "./checkpair"
TRIALS_PER_PAIR = 10000

def run_trials(cpu_A, cpu_B, trials):
    proc = subprocess.run([CHECKER_PATH, str(cpu_A), str(cpu_B), str(trials)], stdout=subprocess.PIPE)
    output = proc.stdout.decode("utf-8")
    latency = int(output)
    return latency

def main():
    cpu_count = len(os.sched_getaffinity(0))
    print(f"Found {cpu_count} CPU(s)")

    graph = nx.Graph()

    bar = Bar("Running Trials", max=((cpu_count*(cpu_count-1)) / 2))

    adj_matrix = [[None] * cpu_count] * cpu_count

    for A, B in itertools.combinations(range(cpu_count), 2):
            latency = run_trials(A, B, TRIALS_PER_PAIR)
            graph.add_edge(A, B, weight=(1.0 / latency))
            bar.next()

    bar.finish()

    weights = nx.get_edge_attributes(graph, "weight")
    labels = { num:str(num) for num in range(cpu_count) }
    edge_cmap = plt.get_cmap("afmhot")

    pos = nx.circular_layout(graph)
    pos = nx.spring_layout(graph, pos=pos)

    nx.draw_networkx_nodes(
            graph, pos,
            nodelist = graph.nodes(),
            node_color = 'black'
            )
    nx.draw_networkx_labels(
            graph, pos,
            labels=labels,
            font_color = 'white')
    nx.draw_networkx_edges(
            graph, pos,
            edgelist = weights.keys(),
            width = [weight * 100.0 for weight in weights.values()],
            edge_color = 'blue'
            )

    plt.box(False)
    plt.show()


if __name__ == "__main__":
    main()

