import csv
import os

filepath_start = "C:/Users/mknaz/Desktop/0224033336 Datasets/"
filepath_node_ending = "200818_0224033336_12-layers_NOD"
filepath_edge_ending = "200818_0224033336_12-layers_EDG"
filepath_format = ".csv"
filepath_node = "".join([filepath_start, filepath_node_ending, filepath_format])
filepath_edge = "".join([filepath_start, filepath_edge_ending, filepath_format])
new_filepath_node = "".join([filepath_start, filepath_node_ending, "-BestsellerScore", filepath_format])

edge_data = []

with open(filepath_edge, "r", encoding="utf-8") as edge_file:
    edge_reader = csv.reader(edge_file)

    for line in edge_reader:
        edge_data.append(line)

    del edge_data[0]

    edge_tuple = [tuple(entry) for entry in edge_data]
    edge_data = list(set(edge_tuple))
    edge_data = [list(entry) for entry in edge_data]

with open(filepath_node, "r", encoding="utf-8") as node_file:
    node_reader = csv.reader(node_file)

    node_data = []

    for node in node_reader:
        node_data.append(node)

    header = node_data[0]
    header.append("bestseller score")
    del node_data[0]

try:
    os.remove(new_filepath_node)
except FileNotFoundError:
    pass

with open(new_filepath_node, "w", encoding="utf-8", newline="") as new_nodes:
    node_writer = csv.writer(new_nodes)
    node_writer.writerow(header)
    node_dict = {}

    for node in node_data:
        key, value = node[0], node[1:]
        node_dict[key] = value

    for node in node_data:
        used_nodes = []
        in_reviews = []
        for edge in edge_data:
            if len(edge) > 1:
                if node[0] == edge[1] and edge[0] not in used_nodes:
                    review_number = node_dict[edge[0]][2]
                    if review_number >= node[2]:
                        in_reviews.append(0)
                    else:
                        in_reviews.append(1)
                    used_nodes.append(edge[0])
        bestseller_score = sum(in_reviews)/6
        node.append(str(bestseller_score))
        if bestseller_score > 1:
            print(in_reviews)
            print(bestseller_score)
            print(node)

        node_writer.writerow(node)
