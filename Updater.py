import csv
from Scraper import check_duplicate, clear_links, get_links, create_link
data = []

with open('recommendations.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        data.append(row)

print(len(data))


def update():
    original_count = len(data)
    with open("recommendations.csv", "a", newline="") as file:
        writer = csv.writer(file)

        for entry in data:

            count = len(data)
            if count > original_count:
                print(count)

            if count >= 1500:
                break
            for item in entry:
                if not check_duplicate(item, data):

                    new_entry = clear_links(get_links(create_link(str(item))))
                    new_entry.insert(0, str(item))
                    data.append(new_entry)

                    with open("recommendations.csv", "a", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerow(new_entry)


update()
