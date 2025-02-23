#! /usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import argparse
import networkx as nx


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path")
    parser.add_argument("output_path")

    args = parser.parse_args()

    input_path = args.input_path
    output_path = args.output_path

    graph = nx.read_graphml(input_path)

    adj_matrix = nx.adjacency_matrix(graph, weight='latency').toarray()

    ax = sns.heatmap(adj_matrix)
    ax.invert_yaxis()

    print(f"Saving Figure to {output_path}")
    plt.savefig(output_path)


if __name__ == "__main__":
    main()
