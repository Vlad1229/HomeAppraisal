class Layer:
    def __init__(self):
        self.input = None
        self.output = None

    def forward_propagation(self, input):
        raise NotImplementedError

    def backward_propagation(self, output_error, learning_rate):
        raise NotImplementedError

    def get_save_struct(self):
        raise NotImplementedError

    def load(self, save_struct):
        raise NotImplementedError
