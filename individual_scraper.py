from selenium import webdriver
import time
from bs4 import BeautifulSoup
import csv
import os
from SampleCompiler import master_data
import random

"""
1. Open a product page and save the recommendations from it
2. Click on a random recommended item
3. Save the recommendations from the item
4. Keep doing 2. and 3. until a certain number is reached
5. Select a different random item and start over

There is an issue with how to make the driver click a random link from the recommendations.
The former approach was to use BeautifulSoup to find the names of the links (how the users see them), and then pass
those names to Selenium to click on them.

The current approach is to select a random link from the recommendations and pass it to the driver to open it. 
That approached turned out 

"""
start = time.time()

sample = master_data()
data = [[["//dp/147363749X/"]]]
raw_links = [["//dp/147363749X/"]]
starting_points = []


def get_links(driver, url):
    links = []
    driver.get(url)
    html = driver.page_source

    sel_soup = BeautifulSoup(html, "html.parser")
    results = sel_soup.find(id="desktop-dp-sims_session-similarities-sims-feature")

    try:
        carousel_items = results.find_all("a", class_="a-link-normal")
        for item in carousel_items:
            links.append(item.get("href"))
    except AttributeError:
        pass

    return links


def delete_reviews(urls):
    for i in [1, 2]:
        for link in urls:
            if link[1:16] == "product-reviews":
                urls.remove(link)

    urls = list(set(urls))

    return urls


def clear_links(urls):
    for i in range(len(urls)):
        link = urls[i]
        link_parts = link.split("/")
        if link[0:5] == "https":
            urls[i] = link_parts[5]  # https links have 2 extra slashes, so the 5th item has to be chosen
        else:
            urls[i] = link_parts[3]

    return urls


def pick_next(urls):
    next_url = ["https://www.amazon.co.uk", random.choice(urls)]
    next_url = "".join(next_url)

    return next_url


def initialise():

    try:
        os.remove("recommendations.csv")
    except FileNotFoundError:
        pass

    with open("recommendations.csv", "a", newline="") as file:
        writer = csv.writer(file)

        for i in range(1000):
            print(i)
            # for entry in data:
            driver = webdriver.Firefox(executable_path="C:/Users/MM/PycharmProjects/geckodriver.exe")
            used_items = []
            # choose random starting point from a large sample
            raw_links = [random.choice(sample)]
            if raw_links[0] in starting_points:  # checks duplicate
                pass
            starting_points.append(raw_links[0])
            for n in range(5):
                next_url = random.choice(raw_links)
                while clear_links([next_url]) in used_items:  # avoids returning to items
                    next_url = random.choice(raw_links)  # randomly picks the recommendation to follow
                used_items.append(clear_links([next_url]))
                scraped_links = delete_reviews(get_links(driver, next_url))
                for link in scraped_links:
                    full_link = ["https://www.amazon.co.uk", link]  # creates a full link
                    full_link = "".join(full_link)
                    raw_links.append(full_link)
                # limits the number of possible recommendations to the last 6 so that only the recommendations from
                # the last item can be followed
                raw_links = raw_links[-6:]
                new_entry = clear_links(scraped_links)
                new_entry.insert(0, str(clear_links([next_url])[0]))
                writer.writerow(new_entry)
            writer.writerow("")

            driver.close()


initialise()

end = time.time()
print(end-start)
