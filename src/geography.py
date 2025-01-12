import csv

from global_vars import regions, subregions

def build_geography():
    with open('data/geography.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 0:
                continue
            if row[0] == 'region':
                regions.append(row[1])
            elif row[0] == 'subregion':
                if row[1] not in subregions:
                    subregions[row[1]] = []
                subregions[row[1]].append(row[2])

    print("Regions:", regions)
    print("Subregions:", subregions)


