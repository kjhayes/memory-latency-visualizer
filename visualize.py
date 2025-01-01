#! /usr/bin/python3

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import argparse
import networkx as nx

class IdentityStrDict(dict):
    def __missing__(self, key):
        return str(key.id)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path")
    parser.add_argument("output_path")

    args = parser.parse_args()

    input_path = args.input_path
    output_path = args.output_path

    graph = nx.read_graphml(input_path)

    weights = nx.get_edge_attributes(graph, "weight")

    pos = nx.circular_layout(graph)
    pos = nx.spring_layout(graph, pos=pos)

    print("Drawing Nodes")
    nx.draw_networkx_nodes(
            graph, pos,
            nodelist = graph.nodes(),
            node_color = 'black'
            )
    print("Drawing Labels")
    nx.draw_networkx_labels(
            graph, pos,
            font_color = 'white')
    print("Drawing Edges")
    nx.draw_networkx_edges(
            graph, pos,
            edgelist = weights.keys(),
            width = [weight * 100.0 for weight in weights.values()],
            edge_color = 'blue'
            )

    print(f"Saving Figure to {output_path}")
    plt.savefig(output_path)


if __name__ == "__main__":
    main()

