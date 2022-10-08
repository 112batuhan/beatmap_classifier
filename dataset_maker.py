from raw_parser import get_dataset_info
from map_data_import import import_categories, import_maps

import numpy as np
import pickle


maps = import_maps()
categories = import_categories()

dataset_y = []
dataset_metadata_X = []
dataset_objectdata_X = []

offset_amount = 10
dataset_length = 200

for (index, map_data) in enumerate(maps):

    try:
        category_id = categories[map_data["main_skillset"]]
        print(str(index)+"/"+str(len(maps)), map_data["beatmap_id"], len(
        dataset_y), map_data["main_skillset"])
    except KeyError:
        print("passing map cuz invalid skillset")
        continue

    try:
        hit_objects = get_dataset_info(map_data["beatmap_id"])
    except:
        print("extreme old map, skipping")
        continue


    for i in range(0, len(hit_objects) - dataset_length, offset_amount):

        dataset_y.append(category_id)
        dataset_objectdata_X.append(hit_objects[i:i+dataset_length])
        metadata = [map_data["diff_sr"],
                    map_data["diff_size"], map_data["diff_approach"]]
        dataset_metadata_X.append(metadata)

    if index > 0 and index % 100 == 0:

        y = np.array(dataset_y)
        metadata = np.array(dataset_metadata_X)
        objectdata = np.array(dataset_objectdata_X)
        print("y:", y.shape, "meta:", metadata.shape,
              "object:", objectdata.shape)

        dataset = {"y": y, "metadata": metadata, "objectdata": objectdata}
        pickle.dump(dataset, open("dataset.p", "wb"))
