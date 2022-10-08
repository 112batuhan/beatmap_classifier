import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import LSTM,Conv1D,MaxPooling1D,GlobalMaxPool1D,BatchNormalization,Dense,Dropout
from tensorflow.keras.models import Sequential
from tensorflow import keras

np.set_printoptions(suppress=True)

dataset = pickle.load(open(r"dataset.p", "rb"))

unique, counts = np.unique(dataset["y"], return_counts=True)
print(dict(zip(unique, counts)))

encoded_labels = []
for label in dataset["y"]:
    new_label = [0]*14
    new_label[label] = 1
    encoded_labels.append(new_label)
y = np.array(encoded_labels)

scaler = MinMaxScaler(feature_range=(0,1))
X = scaler.fit_transform(dataset["objectdata"].reshape(dataset["objectdata"].shape[0], -1)).reshape(dataset["objectdata"].shape)
pickle.dump(scaler, open("test_data/scaler.p","wb"))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(X_train.shape)
print(y_train)

model = Sequential()
model.add(LSTM(80, input_shape=(200,7), return_sequences=True,name='lstm_layer'))
model.add(Conv1D(filters=80, kernel_size=3, padding='same', activation='relu', kernel_initializer='he_uniform'))
model.add(MaxPooling1D(3))
model.add(GlobalMaxPool1D())
model.add(BatchNormalization())
model.add(Dense(100, activation="relu", kernel_initializer='he_uniform'))
model.add(Dropout(0.2))
model.add(Dense(50, activation="relu", kernel_initializer='he_uniform'))
model.add(Dropout(0.2))
model.add(Dense(14, activation="softmax", kernel_initializer='glorot_uniform'))


model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
callback = keras.callbacks.EarlyStopping(monitor='loss', patience=5)
model_info_2 = model.fit(X_train,y_train, epochs=250, batch_size=32,  validation_data=(X_test, y_test), callbacks=[callback])

model.save("test_data/model")