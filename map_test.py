from raw_parser import get_dataset_info
from map_data_import import import_categories

import numpy as np
import pickle
from tensorflow import keras
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler

np.set_printoptions(suppress=True)

def get_predictions(beatmap_id):

    scaler = pickle.load(open(r"test_data/scaler.p", "rb"))

    try:
        hit_objects = get_dataset_info(beatmap_id)
    except:
        print("extreme old map, skipping")


    offset_amount = 1
    dataset_length = 200
    test_data = []
    for i in range(0, len(hit_objects) - dataset_length, offset_amount):
        test_data.append(hit_objects[i:i+dataset_length])
    test_data = np.array(test_data)

    scaled_test = scaler.transform(test_data.reshape(test_data.shape[0], -1)).reshape(test_data.shape)

    model = keras.models.load_model("test_data/model")
    predictions = model.predict(scaled_test)

    summed = np.sum(predictions, axis=0)
    final_eval = summed / predictions.shape[0]

    ind = np.argpartition(final_eval, -5)[-5:]

    categories = import_categories()
    categories = {v: k for k, v in categories.items()}

    final_verdict = {}
    for category, val in zip(ind,final_eval[ind]):
        final_verdict[categories[category]] = val

    final_verdict = sorted(final_verdict.items(), key=lambda x: x[1], reverse=True)
    return final_verdict

if __name__ == "__main__":

    beatmap_id = 2502889
    get_predictions(beatmap_id)
