import time

import numpy as np
import math
import pickle
from ada_boost import AdaBoost

import utils


class ViolaJones:
    def __init__(self, layers):
        assert isinstance(layers, list)
        self.layers = layers
        self.alphas = []
        self.clfs = []

    def train2(self, X, y):
        """
        :param X: Images 19 x 19 - its important that all images have the same size
        :param y: label for image:
        1 - image is positive (has face)
        0 - doesnt have image
        :return:
        """
        img_h, img_w = X[0].shape
        pos_idxs, neg_idxs = np.where(y == 1)[0], np.where(y == 0)[0]

        #Preparing data stage
        print('Hello, the training began!')
        start_training_time = time.time()

        #calculate size of dataset
        pos_count, neg_count = np.sum(y), len(y) - np.sum(y)
        print("Dataset - faces: {}, non-faces: {}".format(pos_count, neg_count))

        #build features
        start_features_time = time.time()
        features = utils.build_features(img_w = img_w, img_h = img_h, min_w=2, min_h=2)
        end_features_time = time.time()
        print("Found {} features in {}".format(len(features), utils.get_pretty_time(start_features_time, end_features_time)))

        #calculate integral images
        X_ii = np.array(list(map(lambda x: utils.to_integral(x), X)), dtype=np.uint32)

        #calculate those features
        start_time_calculation = time.time()
        X_f = utils.apply_features(X_ii, features)
        end_time_calculation = time.time()
        print("Calculated features in time: {}".format(utils.get_pretty_time(start_time_calculation, end_time_calculation)))
        for t in self.layers:
            print('Training adaboost for T = {}'.format(t))
            start_layer = time.time()
            trained_idx = np.concatenate([pos_idxs, neg_idxs])
            np.random.permutation(len(trained_idx))
            clf = AdaBoost(T=t)
            clf.train(X_f, y, features, X_ii)
            self.clfs.append(clf)

            false_positive_idx = []

            for n_idx in neg_idxs:
                if self.classify(X[n_idx]) == 1:
                    false_positive_idx.append(n_idx)

            false_positive_idx = np.array(false_positive_idx)
            end_layer = time.time()
            print('Training adaboost for T = {} finished in {} with {} false positive classified'.format(t, utils.get_pretty_time(
                start_layer, end_layer), len(false_positive_idx)))

        end_training_time = time.time()
        total_time = end_training_time - start_training_time
        print('Training finished in {}'.format(total_time))



    def get_pos_neg_indeces(self, y):
        pos = []
        neg = []
        for idx, label in enumerate(y):
            if label == 1:
                pos.append(idx)
            else:
                neg.append(idx)
        return pos, neg





    def classify(self, image):
        """
        If a no-face is found, reject now. Else, keep looking.
        """

        return self.classify_ii(utils.to_integral(image))

    def classify_ii(self, ii):
        """
        If a no-face is found, reject now. Else, keep looking.
        """
        for clf in self.clfs:  # ViolaJones
            if clf.classify(ii) == 0:
                return 0
        return 1


    @staticmethod
    def load(filename):
        """
        A static method which loads the classifier from a pickle
          Args:
            filename: The name of the file (no file extension necessary)
        """
        with open(filename + ".pkl", 'rb') as f:
            return pickle.load(f)






