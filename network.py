import tensorflow as ts
from tensorflow import keras
import numpy as np


class Network:
    def __init__(self):
        self.model = keras.Sequential()
        dense1 = keras.layers.Dense(5, activation="relu", name="dense_1", input_dim=3)
        self.model.add(dense1)
        dense2 = keras.layers.Dense(5, activation="relu", name="dense_2")
        self.model.add(dense2)
        output = keras.layers.Dense(1, activation="softmax", name="prediction")
        self.model.add(output)

    def test(self):
        print(self.model.weights)
        print(self.model.predict([[1,0.5,0.4],[4,5,2], [-1,-1,-1]]))


if __name__ == "__main__":
    testobject = Network()
    testobject.test()
