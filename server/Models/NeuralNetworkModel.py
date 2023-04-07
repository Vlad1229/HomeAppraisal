import numpy as np
import json

from keras.layers import Concatenate, Dense, Input
from keras.models import Model
from keras.callbacks import EarlyStopping

class NeuralNetworkModel:
    def __init__(self, dwelling_indexes, region_indexes):
        self.dwelling_indexes = dwelling_indexes
        self.region_indexes = region_indexes
        self.build()

    def standardize_data(self, train_data, test_data):
        mean = train_data.mean(axis=0)
        train_data -= mean
        std = train_data.std(axis=0)
        train_data /= std

        test_data -= mean
        test_data /= std
        return train_data, test_data

    def build(self):
        input_1 = Input(shape=(self.region_indexes.shape[0], ))
        hidden_1 = Dense(64, activation='relu')(input_1)
        output_1 = Dense(1, activation='relu')(hidden_1)
        input_2 = Input(shape=(self.dwelling_indexes.shape[0], ))
        concat_2 = Concatenate()([output_1, input_2])
        hidden_2 = Dense(64, activation='relu')(concat_2)
        output_2 = Dense(1)(hidden_2)
        self.model = Model(inputs=[input_1, input_2], outputs=[output_2])
        self.model.compile(loss='mse', metrics=['mae'])

    def region_predict(self, input_data):
        self.model.predict(input_data)
        return output

    def dwelling_predict(self, input_data):
        self.model.pre
        return output

    def fit(self, x_train, y_train, x_test, y_test):
        x_train, x_test = self.standardize_data(x_train, x_test)

        callback = EarlyStopping(
            monitor="val_loss",
            patience=10
        )

        self.model.fit(x=[x_train[:, self.region_indexes], x_train[:, self.dwelling_indexes]], y=y_train, batch_size=64,
                       epochs=200, validation_data=([x_train[:, self.region_indexes], x_train[:, self.dwelling_indexes]], y_train),
                       callbacks=[callback])

        self.region_model

    def save_model(self, path):


    def load_model(self, path):

