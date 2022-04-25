import os
import cv2
import numpy as np


class Adaboost(object):
    def __init__(self):
        self.T = 10
        self.pos_count = 2429
        self.neg_count = 4305
        self.pos_count_test = 22
        self.neg_count_test = 33



    def train(self, dataset):
        weights = np.zeros(len(dataset))
        X = []
        y = []
        for i in range(len(dataset)):
            X.append(dataset[i][0])
            y.append(dataset[i][1])
        print('Setting initial weights')
        for x in range(len(dataset)):
            if dataset[x][1] == 1:
                weights[x] = 1.0 / (2 * self.pos_count_test)
            else:
                weights[x] = 1.0 / (2 * self.neg_count_test)

        for t in range(self.T):
            weights = weights / np.linalg.norm(weights)
            weak_classifiers = self.train_week(X, y, weights)




    def train_week(self, X, y, weights):
        t_plus, t_minus = 0, 0
        for w, label in zip(weights, y):
            if y == 1:
                t_plus += w
            else:
                t_minus += w
        classifiers = []
        total_features = len(X[0])*len(X)
        for index, feature in enumerate(X):
            applied_feature = sorted(zip(weights, feature, y), key=lambda x: x[1])


        return classifiers




