import csv
import numpy as np
from collections import Counter

cluster_file = "C:/Users/mknaz/Desktop/200820_1610391071_Clusters_Res-0.2.csv"
cluster_info = "C:/Users/mknaz/Desktop/200820_1610391071_Cluster_Analysis_Res-0.2.csv"
cluster_data = []

with open(cluster_file, "r", encoding="utf-8") as clusters:
    cluster_reader = csv.reader(clusters)

    for entry in cluster_reader:
        cluster_data.append(entry)

    del cluster_data[0]

while [] in cluster_data:
    cluster_data.remove([])

cluster_data = np.array(cluster_data, dtype=object)

with open(cluster_info, "w", newline="", encoding="utf-8") as info:
    writer = csv.writer(info)
    writer.writerow(["Cluster number", "Cluster size",
                     "c1 1 name", "c1 1 count", "c1 1 percentage",
                     "c1 2 name", "c1 2 count", "c1 2 percentage",
                     "c2 1 name", "c2 1 count", "c2 1 percentage",
                     "c2 2 name", "c2 2 count", "c2 2 percentage",
                     "c3 1 name", "c3 1 count", "c3 1 percentage",
                     "c3 2 name", "c3 2 count", "c3 2 percentage",])

    # finds the number of clusters
    cluster_list = cluster_data[:, -1]
    cluster_list = list(map(int, cluster_list))
    cluster_count = max(cluster_list)

    for i in range(cluster_count + 1):
        cluster_size = 0
        category_1_list = []
        category_2_list = []
        category_3_list = []
        for entry in cluster_data:
            if int(entry[-1]) == i:
                category_1_list.append(entry[7])
                category_2_list.append(entry[8])
                category_3_list.append(entry[9])
                cluster_size += 1
        print("_______________________________________________________________________________________________________")
        category_1_count = Counter(category_1_list)
        category_2_count = Counter(category_2_list)
        category_3_count = Counter(category_3_list)
        print(category_1_count)
        print(category_2_count)
        print(category_3_count)

        category_1_keys = sorted(category_1_count, key=category_1_count.get, reverse=True)
        if len(category_1_keys) > 1:
            category_1_key_0 = category_1_keys[0]
            category_1_key_1 = category_1_keys[1]
        elif len(category_1_keys) == 1:
            category_1_key_0 = category_1_keys[0]
            category_1_key_1 = "N/A"
        else:
            category_1_key_0 = "N/A"
            category_1_key_1 = "N/A"

        category_1_first = category_1_count[category_1_key_0]
        category_1_second = category_1_count[category_1_key_1]

        category_2_keys = sorted(category_2_count, key=category_2_count.get, reverse=True)
        if len(category_2_keys) > 1:
            category_2_key_0 = category_2_keys[0]
            category_2_key_1 = category_2_keys[1]
        elif len(category_1_keys) == 1:
            category_2_key_0 = category_2_keys[0]
            category_2_key_1 = "N/A"
        else:
            category_2_key_0 = "N/A"
            category_2_key_1 = "N/A"

        category_2_first = category_2_count[category_2_key_0]
        category_2_second = category_2_count[category_2_key_1]

        category_3_keys = sorted(category_3_count, key=category_3_count.get, reverse=True)
        if len(category_3_keys) > 1:
            category_3_key_0 = category_3_keys[0]
            category_3_key_1 = category_3_keys[1]
        elif len(category_3_keys) == 1:
            category_3_key_0 = category_3_keys[0]
            category_3_key_1 = "N/A"
        else:
            category_3_key_0 = "N/A"
            category_3_key_1 = "N/A"

        category_3_first = category_3_count[category_3_key_0]
        category_3_second = category_3_count[category_3_key_1]

        new_entry = [i, cluster_size,
                     category_1_key_0, category_1_first, category_1_first / cluster_size,
                     category_1_key_1, category_1_second, category_1_second / cluster_size,
                     category_2_key_0, category_2_first, category_2_first / cluster_size,
                     category_2_key_1, category_2_second, category_2_second / cluster_size,
                     category_3_key_0, category_3_first, category_3_first / cluster_size,
                     category_3_key_1, category_3_second, category_3_second / cluster_size]

        writer.writerow(new_entry)

