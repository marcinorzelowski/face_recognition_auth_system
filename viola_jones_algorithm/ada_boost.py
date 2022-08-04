import numpy as np
from weak_classifier import WeakClassifier
import math




class AdaBoost():
    def __init__(self, T):
        """
        :param T: Number of weak classifier we want to get from an algorithm
        """
        self.T = T
        self.alphas = []
        self.clfs = []

    def train(self, X, y, features, X_ii):
        """

        :param X: Image data in a form (feature, integral_image)
        :param y: Labels for images
        :return:
        """
        pos_count, neg_count = np.sum(y), len(y) - np.sum(y)

        #setup initial weigths
        print('Setting up initial weights.')
        weights = np.zeros(len(y))


        for i, label in enumerate(y):
            if label == 1:
                weights[i] = 1.0 / (2 * pos_count)
            else:
                weights[i] = 1.0 / (2 * neg_count)

        for t in range(self.T):
            print('Training {} classifier'.format(t + 1))
            weights = weights / np.sum(weights)
            weak_classifiers = self.train_week(X, y, features, weights)
            clf, error, accuracy = self.select_best(weak_classifiers, weights, X_ii, y)
            beta = error / (1.0 - error)
            for i in range(len(accuracy)):
                weights[i] = weights[i] * (beta ** (1 - accuracy[i]))
            alpha = math.log(1.0 / beta)
            self.alphas.append(alpha)
            self.clfs.append(clf)

    def train_week(self, X, y, features, weights):
        total_pos_weights, total_neg_weights = 0, 0
        trained_classifiers = []

        for w, label in zip(weights, y):
            if label == 1:
                total_pos_weights += w
            else:
                total_neg_weights += w

        for i, feature in enumerate(X):
            if len(trained_classifiers) % 10000 == 0:
                print('Trained {} out of {} weak classifiers'.format(len(trained_classifiers), len(X) ))
            clf = WeakClassifier(features[i])
            clf.train(feature, y, weights, total_pos_weights, total_neg_weights)
            trained_classifiers.append(clf)
        return trained_classifiers

    def select_best(self, classifiers, weights, X_ii, y):

        best_clf, best_error, best_accuracy = None, float('inf'), None

        for i, clf in enumerate(classifiers):
            error, accuracy = 0, []
            for x, y_i, w in zip(X_ii, y, weights):
                correctness = abs(clf.classify(x) - y_i)
                accuracy.append(correctness)
                error += w * correctness
            error = error / len(X_ii)
            if error < best_error:
                best_clf, best_error, best_accuracy = clf, error, accuracy
        return best_clf, best_error, best_accuracy



    def classify(self, X):
        total = sum(list(map(lambda x: x[0] * x[1].classify(X), zip(self.alphas, self.clfs))))  # Weak classifiers
        return 1 if total >= 0.5 * sum(self.alphas) else 0






