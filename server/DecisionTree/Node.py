import numpy as np


class Node:

    def __init__(self, x, y, indexes, min_leaf=5):
        self.x = x
        self.y = y
        self.indexes = indexes
        self.min_leaf = min_leaf
        self.row_count = len(indexes)
        self.col_count = x.shape[1]
        self.value = np.mean(y[indexes])
        self.score = float('inf')
        self.find_split()

    def find_split(self):
        for feature in range(self.col_count):
            self.find_better_split(feature)

        if self.is_leaf():
            return

        x = self.split_col()
        lhs = np.nonzero(x <= self.split)[0]
        rhs = np.nonzero(x > self.split)[0]
        self.lhs = Node(self.x, self.y, self.indexes[lhs], self.min_leaf)
        self.rhs = Node(self.x, self.y, self.indexes[rhs], self.min_leaf)

    def find_better_split(self, feature):

        x = self.x[self.indexes, feature]

        for i in range(self.row_count):
            lhs = x <= x[i]
            rhs = x > x[i]
            if rhs.sum() < self.min_leaf or lhs.sum() < self.min_leaf:
                continue

            curr_score = self.find_score(lhs, rhs)
            if curr_score < self.score:
                self.feature = feature
                self.score = curr_score
                self.split = x[i]

    def find_score(self, lhs, rhs):
        y = self.y[self.indexes]
        lhs_std = y[lhs].std()
        rhs_std = y[rhs].std()
        return lhs_std * lhs.sum() + rhs_std * rhs.sum()

    def split_col(self):
        return self.x[self.indexes, self.feature]

    def is_leaf(self):
        return self.score == float('inf')

    def predict(self, x):
        return np.array([self.predict_row(xi) for xi in x])

    def predict_row(self, xi):
        if self.is_leaf():
            return self.value

        node = self.lhs if xi[self.feature] <= self.split else self.rhs
        return node.predict_row(xi)
