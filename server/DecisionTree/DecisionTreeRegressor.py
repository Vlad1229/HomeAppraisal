import numpy as np
from DecisionTree.Node import Node


class DecisionTreeRegressor:

    def fit(self, x, y, min_leaf=5):
        self.dtree = Node(x, y, np.array(np.arange(len(y))), min_leaf)
        return self

    def predict(self, x):
        return self.dtree.predict(x)
