from Layers.Layer import Layer
from Functions.Activation import tanh, tanh_prime


def get_activation_func(activation):
    if activation == "tanh":
        return tanh


def get_activation_prime_func(activation):
    if activation == "tanh":
        return tanh_prime


class ActivationLayer(Layer):
    def __init__(self, activation="tanh"):
        super().__init__()
        self.activation_name = activation
        self.activation = get_activation_func(activation)
        self.activation_prime = get_activation_prime_func(activation)

    def forward_propagation(self, input_data):
        self.input = input_data
        self.output = self.activation(self.input)
        return self.output

    def backward_propagation(self, output_error, learning_rate):
        return self.activation_prime(self.input) * output_error

    def get_save_struct(self):
        return {"type": "activation", "activation": self.activation_name}

    def load(self, save_struct):
        self.activation_name = save_struct["activation"]
        self.activation = get_activation_func(self.activation_name)
        self.activation_prime = get_activation_prime_func(self.activation_name)
        return self
