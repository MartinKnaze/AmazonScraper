from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import csv
import os
import time
from datetime import datetime
from random import randint, choice
from Scraper import check_duplicate, initialise_scraping, create_link, get_names, get_links, clear_links
import html
from SampleCompiler import master_data
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Driver options
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

dataset = master_data()

start = time.time()
date = str(datetime.today()).split(" ")[0]
date = date.replace("-", "")
date = date[2:]

initial_id = "0140449280"
# initial_id = choice(dataset)
data = [[str(initial_id)]]
node_data = []
layers = 4
cookies = True

if cookies:
    edge_file = [date, "_", str(initial_id), "_", str(layers), "-layers_EDG.csv"]
    node_file = [date, "_", str(initial_id), "_", str(layers), "-layers_NOD.csv"]
else:
    edge_file = [date, "_no-cookies_", str(initial_id), "_", str(layers), "-layers_EDG.csv"]
    node_file = [date, "_no-cookies_", str(initial_id), "_", str(layers), "-layers_NOD.csv"]

edge_file = "".join(edge_file)
node_file = "".join(node_file)


def get_reviews(soup, given_ids):

    results = soup.find(id="acrCustomerReviewText")
    results = str(results)

    try:
        review_number = results.split(">")[1]
        review_number = review_number.split(" rating")[0]
        review_number = review_number.replace(",", "")
        review_number = int(review_number)
    except IndexError:
        review_number = 0

    reviews = [review_number]

    results = soup.find_all(class_="a-size-small a-link-normal")

    ids = []
    for id in given_ids:
        ids.append(id)
    del ids[0]

    used_ids = []  # will use this to check for duplication

    for id in ids:
        number = "n/a"
        for result in results:
            result = str(result)
            if "product-reviews" in result:
                if id in used_ids:  # prevents data duplication
                    pass
                elif str(id) in result:
                    number = result.split("</a>")[-2]
                    number = number.split(">")[-1]
                    number = number.replace(",", "")
                    try:
                        number = int(number)
                    except ValueError:
                        print("ERROR AVOIDED!!!")
                        print(results)
                        print(review_number)
                        print("_______________")
                    reviews.append(number)
                    used_ids.append(id)
        if number == "n/a":
            reviews.append(0)

    return reviews


def get_category(soup):

    try:
        results = soup.find(id="wayfinding-breadcrumbs_feature_div")
        results = results.find_all(class_="a-link-normal a-color-tertiary")
        results = str(results)
        # results = results.split("a-link-normal a-color-tertiary")
        results = results.split("</a>")

        categories = []

        for result in results:
            try:
                category = str(result)
                category = category.split(">")[1]
                # category = category.split("<")[0]
                category = category.strip()
                category = category.replace(",", "")
                category = html.unescape(category)

                categories.append(category)
            except IndexError:
                pass

        return categories

    except AttributeError:
        pass


def master():

    print("START: " + initial_id)

    starting_items = []
    written_nodes = []
    duplicate_count = 0

    for file in [edge_file, node_file]:
        try:
            os.remove(file)
        except FileNotFoundError:
            pass

    with open(edge_file, "a", newline="", encoding="utf-8") as edges:
        edge_writer = csv.writer(edges)
        edge_writer.writerow(["Source", "Target"])

        with open(node_file, "a", newline="", encoding="utf-8") as nodes:
            nodes_writer = csv.writer(nodes)
            nodes_writer.writerow(["Id", "Label", "Reviews", "Layer",
                                   "Review difference", "Review score",
                                   "category 1", "category 2", "category 3"])

            # The driver is here when we scrape with cookies
            if cookies:
                driver = webdriver.Firefox(executable_path="C:/Users/mknaz/PycharmProjects/geckodriver.exe",
                                          options=options)
                driver.delete_all_cookies()

            for layer in range(layers):
                for entry in data:
                    for item in entry:
                        if item not in starting_items:
                            starting_items.append(item)
                if layer == 0:
                    del data[0]
                # starting_items = list(set(starting_items))
                for item in starting_items:
                    if check_duplicate(item, data):
                        duplicate_count += 1
                    else:
                        # the scraping and saving block

                        # The driver is here when scraping without cookies
                        if not cookies:
                            driver = webdriver.Firefox(executable_path="C:/Users/mknaz/PycharmProjects/geckodriver.exe")
                            #                            options=options)

                        soup = initialise_scraping(driver, create_link(str(item)))

                        if cookies and layer == 0:
                            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "sp-cc-accept"))).click()

                        adjacency_entry = clear_links(get_links(soup))

                        if layer < (layers - 1):
                            for target in adjacency_entry:
                                edge = [str(item), str(target)]
                                edge_writer.writerow(edge)

                        adjacency_entry.insert(0, str(item))
                        data.append(adjacency_entry)

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

                        if adjacency_entry[0] not in written_nodes:
                            node_entry = [adjacency_entry[0], names[0], review_numbers[0],
                                          layer, review_diff, review_score]
                            node_entry.extend(category_list)  # appends the categories
                            written_nodes.append(adjacency_entry[0])
                            nodes_writer.writerow(node_entry)
                            print("Wrote: " + str(node_entry))

                        print("____________________________________________________")
                        for cookie in driver.get_cookies():
                            print(cookie)
                        print("____________________________________________________")

                        if not cookies:
                            driver.close()

                        # second iteration to make sure the first group of nodes is written before starting the new one
                        """
                        if layer == (layers - 1):
                            for i in range(len(adjacency_entry)):
                                if adjacency_entry[i] not in written_nodes:
                                    if adjacency_entry[i] not in starting_items:
                                        try:
                                            node_entry = [adjacency_entry[i], names[i],
                                                          review_numbers[i], layer + 1, "", "", "", "", ""]
                                            written_nodes.append(adjacency_entry[i])
                                            nodes_writer.writerow(node_entry)
                                            # print("Wrote: " + str(node_entry))
                                        except IndexError:  # handles the case when not all names were scraped
                                            node_entry = [adjacency_entry[i], adjacency_entry[i],
                                                          review_numbers[i], layer + 1, "", "", "", "", ""]
                                            written_nodes.append(adjacency_entry[i])
                                            nodes_writer.writerow(node_entry)
                                        # if it is the last layer, it also writes the nodes without review scores
                                        # -1 is there because the iteration does not include the last value
                                        # length comparison to force the scraper to first finish all possible iterations
                                        # of the previous if condition
                        """
                        print("Layer: " + str(layer) + " | Item: " + str(len(data)) + "/" + str(len(starting_items)))

            for item in data:
                print(item)

            if cookies:
                driver.close()

    print(len(data))
    print("DUPLICATES: " + str(duplicate_count))


master()

end = time.time()
# print(end - start)
