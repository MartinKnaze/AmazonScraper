from Scraper import create_link, initialise_scraping, clear_links, get_links
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
from random import randint, choice
from SampleCompiler import master_data
from datetime import datetime
from bs4 import BeautifulSoup
import time
import csv
import os


"""
This script will scrape the data for our bipartite graphs.
It will scrape "sequentially," meaning that it will scrape the starting point, than click on one of its recommendations,
then save the recommendations of that item. The number of layers it will go through before scraping the final set of
recommendations will be set upfront.

It would also be interesting to do this without clearing the links.

"""

# Driver options
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")



start = time.time()
date = str(datetime.today()).split(" ")[0]
date = date.replace("-", "")
date = date[2:]

# Generates a random starting point, would need my previous datasets to use this
dataset = master_data()
initial_id = choice(dataset)

# initial_id = "0140449280"
layers = 4

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

starting_ids = (initial_id, )  # "014044517X"

sequential_data = {starting_ids: "", }
used_keys = []
updated_keys = []
saved_keys = []

count = 0
old_len = 0


def show_time(count, layer_start):
    if count % 5 == 0:
        elapsed = time.time() - start
        hours, rem = divmod(elapsed, 3600)
        minutes, seconds = divmod(rem, 60)
        print("ELAPSED: ", "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))

        hours, rem = divmod(time.time() - layer_start, 3600)
        minutes, seconds = divmod(rem, 60)
        print("LAYER TIME ELAPSED: ", "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))

        predicted = (time.time() - layer_start) * ((len(sequential_data) - old_len - count) / count)
        hours, rem = divmod(predicted, 3600)
        minutes, seconds = divmod(rem, 60)
        print("REMAINING: ", "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))


def find_max_finished_layer(data):
    max_finished_layer = len(max(data.keys(), key=len))
    finished = True
    if max_finished_layer != 0:
        for i in range(max_finished_layer, 0, -1):
            finished = True
            for key in data:
                if len(key) == i:
                    if data[key] == "":
                        finished = False
            if finished:
                max_finished_layer = i
                break
        if not finished:
            max_finished_layer = 0

    return max_finished_layer


def define_sequences(data, used):
    to_scrape = []

    max_finished_layer = find_max_finished_layer(data)

    for key in data:
        if key not in used:
            if len(key) == (max_finished_layer + 1):
                if data[key] == "":
                    to_scrape.append(key)
                    used.append(key)

    return to_scrape


def scrape_sequentially(sequences, saved_keys):

    outdict = {}
    last_saved = time.time()
    with open(bip_edge_file, "a", newline="", encoding="utf-8") as bip_edges:
        bip_edge_writer = csv.writer(bip_edges)
        # bip_edge_writer.writerow(["Source", "Target"])

        for sequence in sequences:
            while sequence not in outdict.keys():
                try:
                    driver = webdriver.Firefox(executable_path="C:/Users/mknaz/PycharmProjects/geckodriver.exe",
                                               options=options)
                    driver.delete_all_cookies()
                    driver.set_page_load_timeout(600)  # Copied from initialise_scraping in Scraper.py
                    for index in range(len(sequence)):
                        # Click on items
                        item = sequence[index]
                        soup = initialise_scraping(driver, create_link(str(item)))
                        # time.sleep(300)
                        if index == 0:  # Only accepts cookies for the first item
                            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "sp-cc-accept"))).click()
                        if index == len(sequence) - 1:  # only scrapes for the last item, - 1 because len will always 1 larger than index
                            adjacency_entry = clear_links(get_links(soup))

                            outdict[sequence] = tuple(adjacency_entry)

                    now = datetime.now().time()
                    last_updated = now.strftime("%H:%M:%S")
                    print("Updated at: ", last_updated, " | Layer: ", str(len(sequence)),
                          " | Finished: ", str(sequences.index(sequence) + 1), " / ", len(sequences))

                    if (time.time() - last_saved) > 60:
                        print("Saved.")
                        for key in outdict:
                            if outdict[key] != "":
                                if key not in saved_keys:
                                    for value in outdict[key]:
                                        entry = [key, value]
                                        bip_edge_writer.writerow(entry)
                                        saved_keys.append(key)

                        last_saved = time.time()

                    driver.delete_all_cookies()
                    driver.quit()

                except TimeoutException:
                    print("Timeout Exception occurred at SequentialScraper.py at: ", datetime.now())
                    print(sequence)
                    driver.quit()
                    continue
                except WebDriverException:
                    print("WebDriver Exception occurred at SequentialScraper.py at: ", datetime.now())
                    print(sequence)
                    driver.quit()
                    continue

        return outdict


def update_dict(data, input_dict):

    throwaway_dict = {}

    data.update(input_dict)

    for key in data:
        updated_keys.append(key)

    # Add new keys to dictionary for the next iteration
    for key in input_dict:
        if input_dict[key] not in updated_keys:
            for value in input_dict[key]:
                # if value not in list(key):  # Prevents clicking on the same item twice
                new_key = list(key)
                new_key = new_key + [value]  # cannot modify tuple, so converts it to list and then back
                new_key = tuple(new_key)
                throwaway_dict[new_key] = ""

    # Deletes duplicate keys so that existing values are not replaced by empty ones
    to_del = []
    for key in throwaway_dict:
        if key in list(data.keys()):
            to_del.append(key)

    # Deletes separately so that the dictionary does not change size during iteration
    for key in to_del:
        del throwaway_dict[key]

    data.update(throwaway_dict)


def master(data):

    for file in [edge_file, tree_edge_file, bip_node_file, bip_edge_file]:
        try:
            os.remove(file)
        except FileNotFoundError:
            pass

    # Writes file for bipartite graph visualisations

        for layer in range(layers):

            print("LAYER: ", str(layer + 1))

            sequences_to_scrape = define_sequences(data, used_keys)
            # print(len(sequences_to_scrape))
            # for key in data:
            #     print(key, data[key])
            new_items = scrape_sequentially(sequences_to_scrape, saved_keys)
            update_dict(data, new_items)


def write_data(data, edge_file, bip_node_file, tree_edge_file, bip_last_edge_file):

    for file in [edge_file, tree_edge_file, bip_node_file]:
        try:
            os.remove(file)
        except FileNotFoundError:
            pass

    max_finished_layer = find_max_finished_layer(data)

    with open(edge_file, "a", newline="", encoding="utf-8") as edges:
        with open(bip_last_edge_file, "a", newline="", encoding="utf-8") as last_edges:
            edge_writer = csv.writer(edges)
            edge_writer.writerow(["Source", "Target"])
            last_edges_writer = csv.writer(last_edges)
            last_edges_writer.writerow(["Source", "Target"])
            for key in data:
                key = list(key)
                if len(key) > 1:
                    for i in range(len(key) - 1):
                        entry = [key[i], key[i + 1]]
                        edge_writer.writerow(entry)
                for value in data[tuple(key)]:
                    entry = [key[-1], value]
                    edge_writer.writerow(entry)
                if len(key) == max_finished_layer - 1:
                    for value in data[tuple(key)]:
                        entry = [key, value]
                        last_edges_writer.writerow(entry)


        with open(bip_node_file, "a", newline="", encoding="utf-8") as bip_nodes:
            bip_node_writer = csv.writer(bip_nodes)
            bip_node_writer.writerow(["id", "layer"])
            with open(tree_edge_file, "a", newline="", encoding="utf-8") as tree_edges:
                tree_edge_writer = csv.writer(tree_edges)
                tree_edge_writer.writerow(["Source", "Target"])
                for key in data:  # Sorts the edges within keys
                    key = list(key)
                    if len(key) > 1:
                        for i in range(len(key) - 1):
                            entry = [key[i], key[i + 1]]
                            source = str(str(i) + "-" + entry[0])
                            target = str(str(i + 1) + "-" + entry[1])
                            print(source, target)
                            tree_edge_writer.writerow([source, target])
                            bip_node_writer.writerow([entry[0], i])
                            bip_node_writer.writerow([entry[1], i + 1])
                for key in data:  # Takes care of the edges between each last item and key and the items it links to
                    for value in data[key]:
                        key = list(key)
                        key_entry = str(layers - 1) + "-" + key[-1]
                        value_entry = str(layers) + "-" + value
                        entry = [key_entry, value_entry]
                        # entry = [key[-1], value]
                        print(entry)
                        tree_edge_writer.writerow(entry)


# First, we will need the full network through which these sequences will be scraped. We need it to prevent bias.
# In effect, the whole process will need to be done twice.

# print(sequential_data)
# print("_______________________________________________________________________________________________________________")

master(sequential_data)
# write_data(sequential_data, edge_file, bip_node_file, tree_edge_file)

end = time.time()
# print(end - start)
