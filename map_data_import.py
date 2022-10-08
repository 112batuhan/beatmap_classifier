import csv

def import_categories():
    categories = {}
    with open('map_source/categories.csv', mode='r') as f:
        reader = csv.reader(f)
        for row in reader:
            categories[row[1]] = int(row[0])
    return categories
   
def import_maps():
    maps = []
    with open('map_source/maps.csv', mode='r') as f:
        reader = csv.reader(f)
        skip_header = True
        for row in reader:
            if skip_header:
                headers = row
                skip_header = False
                continue
            
            map_dict = {}
            for (header, data) in zip(headers, row):
                map_dict[header] = data
            maps.append(map_dict)
    return maps
