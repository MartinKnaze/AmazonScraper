from ExtensiveScraper import get_category
from Scraper import initialise_scraping, create_link, get_names
import csv
from selenium import webdriver
import os

old_node_file = "C:/Users/mknaz/PycharmProjects/Scraper/200809_0575093366_16-layers_NOD - Copy.csv"
new_node_file = "C:/Users/mknaz/PycharmProjects/Scraper/200809_0575093366_16-layers_NOD_CAT.csv"

nodes = []
count = 0

with open(old_node_file, "r", encoding="utf-8") as old_nodes:
    node_reader = csv.reader(old_nodes)

    for entry in node_reader:
        nodes.append(entry)

    header = nodes[0]

    del nodes[0]

    length = len(nodes)

try:
    os.remove(new_node_file)
except FileNotFoundError:
    pass

with open(new_node_file, "w", encoding="utf-8") as new_nodes:
    node_writer = csv.writer(new_nodes)

    # header.extend(["category 1", "category 2", "category 3"])
    node_writer.writerow(header)

    driver = webdriver.Firefox(executable_path="C:/Users/mknaz/PycharmProjects/geckodriver.exe")

    for entry in nodes:
        count += 1
        item = entry[0]

        if "" in entry[-3:] or len(entry[1]) == 10:
            soup = initialise_scraping(driver, create_link(str(item)))

            if "" in entry[-3]:
                entry = entry[:-3]
                category_list = get_category(soup)
                try:
                    while len(category_list) < 3:
                        category_list.append("")
                    while len(category_list) > 3:
                        category_list.pop(-1)
                    entry.extend(category_list)
                except TypeError:
                    entry.extend(["", "", ""])

            if len(entry[1]) == 10:
                del entry[1]
                name = get_names(soup)[0]
                entry.insert(1, name)

        print(entry)
        print(str(count), "/", str(length))

        node_writer.writerow(entry)

driver.close()
