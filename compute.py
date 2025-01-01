#! /usr/bin/python3

import subprocess
import os
import networkx as nx
import itertools
import argparse
from progress.bar import Bar

CHECKER_PATH = "./checkpair"
TRIALS_PER_PAIR = 10000

def run_trials(cpu_A, cpu_B, trials):
    proc = subprocess.run([CHECKER_PATH, str(cpu_A), str(cpu_B), str(trials)], stdout=subprocess.PIPE)
    output = proc.stdout.decode("utf-8")
    del proc # Try and avoid leaving zombies around
    latency = int(output)
    return latency

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")

    args = parser.parse_args()

    path = args.path

    cpu_count = len(os.sched_getaffinity(0))
    print(f"Found {cpu_count} CPU(s)")

    graph = nx.Graph()

    bar = Bar("Running Trials", max=((cpu_count*(cpu_count-1)) / 2))

    for A, B in itertools.combinations(range(cpu_count), 2):
            latency = run_trials(A, B, TRIALS_PER_PAIR)
            graph.add_edge(A, B, weight=(1.0 / latency))
            bar.next()

    bar.finish()

    nx.write_graphml(graph, path)


if __name__ == "__main__":
    main()


