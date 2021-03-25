import csv
from Scraper import create_link, initialise_scraping, clear_links, get_links
from SequentialScraper import scrape_sequentially, update_dict, define_sequences, master, write_data, \
    find_max_finished_layer
from ast import literal_eval as make_tuple
from selenium.webdriver.firefox.options import Options
from datetime import datetime
import time
import os

# Driver options
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

start = time.time()
date = str(datetime.today()).split(" ")[0]
date = date.replace("-", "")
date = date[2:]

input_file = "201120_BIP_0140449280_6-layers_EDG.csv"
initial_id = input_file.split("_")[2]
layers = int(input_file.split("_")[3].split("-")[0])
temp_data = []
data = {}
used_keys = []

# Edge file for bipartite graphs
bip_edge_file = [date, "_BIP_", str(initial_id), "_", str(layers), "-layers_UPD_EDG.csv"]
bip_edge_file = "".join(bip_edge_file)

# Edge file for the last layer for bipartite graphs
bip_last_edge_file = [date, "_BIP_LST_", str(initial_id), "_", str(layers), "-layers_EDG.csv"]
bip_last_edge_file = "".join(bip_last_edge_file)

# Node file for bipartite graphs
bip_node_file = [date, "_BIP_", str(initial_id), "_", str(layers), "-layers_NOD.csv"]
bip_node_file = "".join(bip_node_file)

# Edge file for tree diagrams
tree_edge_file = [date, "_TREE_", str(initial_id), "_", str(layers), "-layers_EDG.csv"]
tree_edge_file = "".join(tree_edge_file)

# Edge file for traditional network graphs
edge_file = [date, "_SEQ_", str(initial_id), "_", str(layers), "-layers_EDG.csv"]
edge_file = "".join(edge_file)


def create_data(file):
    with open(file, "r", encoding="utf-8") as in_file:
        has_header = csv.Sniffer().has_header(in_file.read(1024))
        in_file.seek(0)
        in_reader = csv.reader(in_file)
        if has_header:
            next(in_reader)
        for entry in in_reader:
            key = make_tuple(entry[0])

            if key not in data.keys():
                data[key] = (entry[1], )
            else:
                value = data[key]
                if entry[1] not in value:
                    value = list(value)
                    value.append(entry[1])
                    value = tuple(value)
                data[key] = tuple(value)
            used_keys.append(key)

    return data

# for key in data:
#     print(key, data[key])


def identify_next_layer(data):
    throwaway_dict = {}

    for key in data:
        for value in data[key]:
            if value not in list(key):
                new_key = [item for item in key]  # cannot modify tuple, so converts it to list and then back
                new_key.append(value)
                new_key = tuple(new_key)
                throwaway_dict[new_key] = ""

    to_del = []
    for key in throwaway_dict:
        if key in list(data.keys()):
            to_del.append(key)

    for key in to_del:
        del throwaway_dict[key]
    to_del = []

    data.update(throwaway_dict)

    # The following lines delete keys that were made too soon to ensure layer integrity
    max_finished_layer = find_max_finished_layer(data)
    print(max_finished_layer)

    for key in data:
        if len(key) > max_finished_layer + 1:
            to_del.append(key)

    for key in to_del:
        del data[key]


# create_data(input_file)
# identify_next_layer(data)

# master(data)
# write_data(edge_file, bip_node_file, tree_edge_file)

