import csv
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from Scraper import check_duplicate, initialise_scraping, create_link, get_names, get_links, clear_links
from ExtensiveScraper import options, get_reviews, get_category


old_edge_file = "200817_0224033336_20-layers_EDG.csv"
old_node_file = "200817_0224033336_20-layers_NOD.csv"

new_edge_file = "200817_0224033336_20-layers_EDG_FIN.csv"
new_node_file = "200817_0224033336_20-layers_NOD_FIN.csv"

edge_data = []
node_data = []

layers = []

with open(old_edge_file, "r", encoding="utf-8") as old_edges:
    edge_reader = csv.reader(old_edges)

    for entry in edge_reader:
        edge_data.append(entry)

    del edge_data[0]

initial_id = edge_data[0][0]
node_data.append(initial_id)
layers.append([initial_id])

written_nodes = []
for layer in layers:
    current_layer = []
    for node in layer:
        for edge in edge_data:
            if node == edge[0]:
                if edge[1] not in current_layer and edge[1] not in written_nodes:
                    current_layer.append(edge[1])
    layers.append(current_layer)
    for node in current_layer:
        written_nodes.append(node)
    # print(len(written_nodes))
    # print(len(current_layer))
    # print(len(layers))
    # print("____________________________________")
    if len(current_layer) == 0:
        break

print(len(layers[-3]))

to_scrape = []
written_nodes = []

for layer in layers:
    to_scrape_local = []
    for node in layer:
        for edge in edge_data:
            if node == edge[0]:
                if edge[1] not in to_scrape_local and edge[1] not in written_nodes:
                    to_scrape_local.append(edge[1])
                    written_nodes.append(edge[1])
    to_scrape.append(to_scrape_local)


with open(new_edge_file, "a", newline="", encoding="utf-8") as edges:
    edge_writer = csv.writer(edges)
    edge_writer.writerow(["Source", "Target"])

    with open(new_node_file, "a", newline="", encoding="utf-8") as nodes:
        nodes_writer = csv.writer(nodes)
        nodes_writer.writerow(["Id", "Label", "Reviews", "Layer",
                                "Review difference", "Review score",
                               "category 1", "category 2", "category 3"])

        for layer in layers[-2:]:

            count = 0

            for item in layer:
                # the scraping and saving block
                driver = webdriver.Firefox(executable_path="C:/Users/mknaz/PycharmProjects/geckodriver.exe",
                                           options=options)
                # driver.minimize_window()

                soup = initialise_scraping(driver, create_link(str(item)))

                adjacency_entry = clear_links(get_links(soup))

                for target in adjacency_entry:
                    edge = [str(item), str(target)]
                    edge_writer.writerow(edge)

                adjacency_entry.insert(0, str(item))

                names = get_names(soup)
                review_numbers = get_reviews(soup, adjacency_entry)

                # category = get_category(soup)

                # calculate whether the recommendations have more reviews than the original
                review_diff = ((sum(review_numbers[1:]) / len(review_numbers[1:])) - review_numbers[0])

                review_score = 0

                # the block that calculates the review score
                for i in review_numbers[1:]:
                    if i > review_numbers[0]:
                        review_score += 1
                    elif i < review_numbers[0]:
                        review_score -= 1

                # the block that gets the categories
                category_list = get_category(soup)
                try:
                    while len(category_list) < 3:
                        category_list.append("")
                    while len(category_list) > 3:
                        category_list.pop(-1)
                except TypeError:
                    category_list = ["", "", ""]

                if item not in written_nodes:
                    node_entry = [item, names[0], review_numbers[0],
                                  len(layers), review_diff, review_score]
                    node_entry.extend(category_list)  # appends the categories
                    written_nodes.append(adjacency_entry[0])
                    count += 1
                    nodes_writer.writerow(node_entry)
                    print("Wrote: " + str(node_entry))
                    # second iteration to make sure the first group of nodes is written before starting the new one

                print("Layer: " + str(layers.index(layer)) + " | Item: " + str(count) + "/" + str(len(layer)))

                driver.close()
