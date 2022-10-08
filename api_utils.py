from raw_parser import get_dataset_info
from map_data_import import import_categories

import numpy as np
import pickle
from tensorflow import keras
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import json


class Predicter:

    def __init__(self):
        self.scaler = pickle.load(open(r"test_data/scaler.p", "rb"))
        self.model = keras.models.load_model("test_data/model")
        self.categories = {v: k for k, v in import_categories().items()}

    def predict(self, beatmap_id, complete_eval=False):

        hit_objects = get_dataset_info(beatmap_id)
        offset_amount = 1
        dataset_length = 200
        test_data = []
        for i in range(0, len(hit_objects) - dataset_length, offset_amount):
            test_data.append(hit_objects[i:i+dataset_length])
        test_data = np.array(test_data)

        scaled_test = self.scaler.transform(test_data.reshape(
            test_data.shape[0], -1)).reshape(test_data.shape)
        predictions = self.model.predict(scaled_test)
        summed = np.sum(predictions, axis=0)
        final_eval = summed / predictions.shape[0]

        final_verdict = {}
        for (index, val) in enumerate(final_eval):
            final_verdict[self.categories[index]] = val
        final_verdict = sorted(final_verdict.items(),
                               key=lambda x: x[1], reverse=True)
        return {key: float(value) for key, value in final_verdict}


def save_to_db(beatmap_id):
    #TODO: make a database and save data there. 
    # This will reduce computational cost in the long run
    pass


def check_in_db(beatmap_id):
    pass


if __name__ == "__main__":

    predicter = Predicter()
    result = predicter.predict(10801, True)
    print(result)
    print(json.dumps(result))
