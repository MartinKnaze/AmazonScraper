import csv
from SequentialUpdater import create_data
from SequentialScraper import write_data

folder = "C:/Users/mknaz/Desktop/"
file = "210102_BIP_1949673162_4-layers_EDG.csv"
filepath = "".join([folder, file])

date = file.split("_")[0]
initial_id = file.split("_")[2]
layers = file.split("_")[3].split("-")[0]

# Edge file for bipartite graphs
bip_edge_file = [date, "_BIP_", str(initial_id), "_", str(layers), "-layers_EDG.csv"]
bip_edge_file = "".join(bip_edge_file)

# Node file for bipartite graphs
bip_node_file = [date, "_BIP_", str(initial_id), "_", str(layers), "-layers_NOD.csv"]
bip_node_file = "".join(bip_node_file)

# Edge file for tree diagrams
tree_edge_file = [date, "_TREE_", str(initial_id), "_", str(layers), "-layers_EDG.csv"]
tree_edge_file = "".join(tree_edge_file)

# Edge file for traditional network graphs
edge_file = [date, "_SEQ_", str(initial_id), "_", str(layers), "-layers_EDG.csv"]
edge_file = "".join(edge_file)

# Edge file for the last layer for bipartite graphs
bip_last_edge_file = [date, "_BIP_LST_", str(initial_id), "_", str(layers), "-layers_EDG.csv"]
bip_last_edge_file = "".join(bip_last_edge_file)

data = create_data(filepath)
write_data(data, edge_file, bip_node_file, tree_edge_file, bip_last_edge_file)

