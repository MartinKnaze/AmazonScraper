import csv
import os

filepath_start = "C:/Users/mknaz/Desktop/0224033336 Datasets/"
filepath_node_ending = "200818_0224033336_12-layers_NOD-BestsellerScore"
filepath_edge_ending = "200818_0224033336_12-layers_EDG"
filepath_format = ".csv"
filepath_node = "".join([filepath_start, filepath_node_ending, filepath_format])
filepath_edge = "".join([filepath_start, filepath_edge_ending, filepath_format])

edge_data = []

with open(filepath_edge, "r", encoding="utf-8") as edge_file:
    edge_reader = csv.reader(edge_file)

    for line in edge_reader:
        edge_data.append(line)

    del edge_data[0]

with open(filepath_node, "r", encoding="utf-8") as node_file:
    node_reader = csv.reader(node_file)

    node_data = []
    layers = []

    for line in node_reader:
        node_data.append(line)
        layers.append(line[3])

    del layers[0]

    layer_number = int(max(layers))
    used_nodes = []

    for layer in range(layer_number):
        new_filepath_node = "".join([filepath_start, filepath_node_ending, "-", str(layer), "-layer", filepath_format])
        new_filepath_edge = "".join([filepath_start, filepath_edge_ending, "-", str(layer), "-layer", filepath_format])

        try:
            os.remove(new_filepath_node)
        except FileNotFoundError:
            pass

        with open(new_filepath_node, "w", encoding="utf-8") as new_nodes:
            node_writer = csv.writer(new_nodes)
            node_writer.writerow(["Id", "Label", "Reviews", "Layer", "Review difference", "Review score",
                                  "Category 1", "Category 2", "Category 3", "Bestseller score"])

            for entry in node_data:
                if entry[3] == str(layer):
                    used_nodes.append(entry[0])
                    node_writer.writerow(entry)

        with open(new_filepath_edge, "w", encoding="utf-8") as new_edges:
            edge_writer = csv.writer(new_edges)
            edge_writer.writerow(["Source", "Target"])

            for entry in edge_data:
                if entry[0] in used_nodes and entry[1] in used_nodes:
                    edge_writer.writerow(entry)

