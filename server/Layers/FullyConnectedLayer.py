from Layers.Layer import Layer
import numpy as np


class FullyConnectedLayer(Layer):
    def __init__(self, input_size, output_size):
        super().__init__()
        self.weights = np.random.rand(input_size, output_size) - 0.5
        self.bias = np.random.rand(1, output_size) - 0.5

    def forward_propagation(self, input_data):
        self.input = input_data
        self.output = np.dot(self.input, self.weights) + self.bias
        return self.output

    def backward_propagation(self, output_error, learning_rate):
        input_error = np.dot(output_error, self.weights.T)
        weights_error = np.dot(self.input.T, output_error)

        self.weights -= learning_rate * weights_error
        self.bias -= learning_rate * output_error
        return input_error

    def get_save_struct(self):
        return {"type": "fully_connected", "weights": self.weights.tolist(), "bias": self.bias.tolist()}

    def load(self, save_struct):
        self.weights = save_struct["weights"]
        self.bias = save_struct["bias"]
        return self
