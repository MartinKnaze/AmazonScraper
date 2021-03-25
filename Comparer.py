import csv
original = []
new = []

original_entries = []
new_entries = []

count = 0

with open('recommendations_original.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        original.append(row)

with open('recommendations.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        new.append(row)

for item in original:
    original_entries.append(item[0])

for item in new:
    new_entries.append(item[0])

for item in original_entries:
    if item in new_entries:
        count += 1

"""
for i in range(0, len(original)):
    print(i)
    if original[i] == new[i]:
        print("SAME")
        count += 1
"""
print(original_entries)
print(new_entries)
print(count)