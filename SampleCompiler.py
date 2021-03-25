import csv
import os


def create_sample(dataset):

    data = []
    sample = []

    with open(dataset, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)

    for row in data:
        for item in row:
            # link = ["https://www.amazon.co.uk//dp/", item]
            # link = "".join(link)
            sample.append(item)

    sample = list(set(sample))

    return sample


def master_data():
    final_sample = []
    for item in os.listdir("C:/Users/mknaz/PycharmProjects/Scraper/book_samples"):
        path = ["C:/Users/mknaz/PycharmProjects/Scraper/book_samples/", str(item)]
        path = "".join(path)
        sample = create_sample(path)
        for item in sample:
            final_sample.append(item)
    final_sample = list(set(final_sample))

    return final_sample
