import numpy as np
import json


class RandomForestModel:
    def __init__(self, dwelling_indexes, region_indexes):
        self.dwelling_indexes = dwelling_indexes
        self.region_indexes = region_indexes
        self.region_layers = []
        self.decision_trees = []

    @staticmethod
    def sample(x):
        n_rows, n_cols = x.shape * 0.7
        samples = np.random.choice(a=n_cols, size=n_cols, replace=True)
        return x[:, samples]

    def load_region_layers(self, path):
        with open(path, 'r') as openfile:
            json_object = json.load(openfile)

        for layer_struct in json_object["region_network"]:
            if layer_struct["type"] == "fully_connected":
                self.region_layers.append(FullyConnectedLayer(0, 0).load(layer_struct))
            elif layer_struct["type"] == "activation":
                self.region_layers.append(ActivationLayer().load(layer_struct))

    def fit(self, x, y, num_trees, min_leaf):
        if len(self.decision_trees) > 0:
            self.decision_trees = []

        region_data = x[:, self.region_indexes]
        region_data = region_data.reshape(region_data.shape[0], 1, region_data.shape[1])
        dwelling_data = x[:, self.dwelling_indexes]

        output = region_data
        for layer in self.region_layers:
            output = layer.forward_propagation(output)

        output = output.reshape(output.shape[0], 1)
        dwelling_data = np.concatenate((output, dwelling_data), axis=1)

        num_built = 0
        while num_built < num_trees:
            clf = DecisionTreeRegressor()
            x_sample = self.sample(dwelling_data)
            clf.fit(x_sample, y)
            self.decision_trees.append(clf)
            num_built += 1

    def predict(self, input_data):
        region_data = input_data[:, self.region_indexes]
        region_data = region_data.reshape(region_data.shape[0], 1, region_data.shape[1])
        dwelling_data = input_data[:, self.dwelling_indexes]

        output = region_data
        for layer in self.region_layers:
            output = layer.forward_propagation(output)

        output = output.reshape(output.shape[0], 1)
        dwelling_data = np.concatenate((output, dwelling_data), axis=1)

        results = []
        for decision_tree in self.decision_trees:
            results += [decision_tree.predict(dwelling_data)]

        return results