from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import os
import time
from random import randint, choice
import html
from SampleCompiler import master_data

"""
Initial product ID: 0141184949

"""
start = time.time()

# dataset = master_data()

# initial_id = id_generator()
# initial_id = choice(dataset)  # "B0787RC6T7" --> Factfulness audiobook
initial_id = "B0799Q4VL5"
data = [[str(initial_id)]]
layers = 7
filename = [str(layers), "-layers_", str(initial_id), ".csv"]
filename = "".join(filename)

sample = []


def id_generator():
    with open('recommendations.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            sample.append(row)

    print(len(sample))
    product_id = sample[randint(1, len(sample))][randint(1, 6)]

    return product_id


def create_link(product_id):
    list_url = ["https://www.amazon.co.uk/dp/", str(product_id)]
    link = "".join(list_url)

    return link


def initialise_scraping(driver, url):
    # Creates the soup so that I can choose what data to collect by creating new functions, independent of this one
    # driver.set_page_load_timeout(600)
    driver.get(url)
    html = driver.page_source

    sel_soup = BeautifulSoup(html, "html.parser")

    return sel_soup


def get_links(soup):
    # Gets the links
    global carousel_links

    results = soup.find(id="desktop-dp-sims_session-similarities-sims-feature")
    try:
        carousel_links = results.find_all("a", class_="a-link-normal")
    except AttributeError:
        pass

    links = []

    for item in carousel_links:
        addition = item.get("href")
        # addition = addition.encode("utf-8")
        links.append(addition)

    return links


def get_names(soup):

    global carousel_names

    def clear_name(item):  # removes the spaces, newlines, and HTML markers from the scraped data
        try:
            name = str(item)
            name = html.unescape(name)
            name = name.split(">")[1]
            name = name.split("<")[0]
            name = name.strip()
            name = name.replace(",", "")

            return name

        except IndexError:
            pass

    names = []
    title_html = soup.find(id="productTitle")
    focal_name = clear_name(title_html)
    names.append(focal_name)

    results = soup.find(id="desktop-dp-sims_session-similarities-sims-feature")

    try:
        found_names = results.find_all("div", class_="p13n-sc-truncate p13n-sc-line-clamp-3")
        for name in found_names:
            if name is not None:
                name = clear_name(name)
                names.append(name)
    except AttributeError:
        pass

    try:
        found_names = results.find_all("div", class_="p13n-sc-truncate p13n-sc-line-clamp-4")
        for name in found_names:
            if name is not None:
                name = clear_name(name)
                names.append(name)
    except AttributeError:
        pass

    try:
        found_names = results.find_all("div", class_="p13n-sc-truncated")
        for name in found_names:
            if name is not None:
                name = clear_name(name)
                names.append(name)
    except AttributeError:
        pass

    results = str(results)
    results = results.split(">")
    order = []

    for name in names:
        for result in results:
            if name in results:
                order.append(results.index(result))

    # print(order)

    return names


def list_unique(array, limit):
    if len(array) >= limit:
        unique_items = []
        for entry in array:
            if array.index(entry) > limit:
                break
            for item in entry:
                unique_items.append(item)

        unique_items = list(set(unique_items))

        return unique_items

    else:
        pass


def clear_links(links):
    for i in [1, 2]:
        for link in links:
            if "product-reviews" in link:
                links.remove(link)

    links = links[1::2]  # takes every other element from list, replaces set which changed order of elements
    new_links = []

    for link in links:
        link_parts = link.split("/")
        new_links.append(link_parts[3])

    return new_links


def check_duplicate(item, data):
    for i in range(len(data)):
        if item == data[i][0]:
            return True


def master():

    print("START:  " + initial_id)

    starting_items = []

    try:
        os.remove(filename)
    except FileNotFoundError:
        pass

    with open(filename, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        driver = webdriver.Firefox(executable_path="C:/Users/MM/PycharmProjects/geckodriver.exe")

        for layer in range(layers):
            for entry in data:
                for item in entry:
                    starting_items.append(item)
            if layer == 0:
                del data[0]
            starting_items = list(set(starting_items))
            print("Layer: " + str(layer))
            for item in starting_items:
                if not check_duplicate(item, data):
                    # the scraping and saving block
                    soup = initialise_scraping(driver, create_link(str(item)))

                    new_entry = clear_links(get_links(soup))
                    new_entry.insert(0, str(item))
                    data.append(new_entry)

                    name_entry = get_names(soup)
                    writer.writerow(name_entry)
                    print("Done " + str(len(data)) + " out of " + str(len(starting_items)))
            for item in data:
                print(item)
            print("__________________________________________________")
            print(len(data))
        driver.close()

    print(len(data))


# master()

end = time.time()
# print(end - start)
