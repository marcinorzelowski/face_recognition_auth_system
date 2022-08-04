import numpy as np


class WeakClassifier:

    def __init__(self, haar_feature=None, threshold=None, polarity=None):
        self.haar_feature = haar_feature
        self.threshold = threshold
        self.polarity = polarity

    def classify(self, ii):
        """
        Classifies an image given its (integral) image "x"
        """
        feature_value = self.haar_feature.compute_value(ii)
        return 1 if self.polarity * feature_value < self.polarity * self.threshold else 0

    def train(self, X, y, weights, total_pos_weights, total_neg_weights):

        # Sort features according to their numeric value
        sorted_features = sorted(zip(weights, X, y), key=lambda a: a[1])

        pos_seen, neg_seen = 0, 0
        sum_pos_weights, sum_neg_weights = 0, 0

        min_error, best_feature, best_threshold, best_polarity = float('inf'), None, None, None
        for w, f, label in sorted_features:
            error = min(sum_neg_weights + (total_pos_weights - sum_pos_weights),
                        sum_pos_weights + (total_neg_weights - sum_neg_weights))

            # Save best values
            if error < min_error:
                min_error = error
                self.threshold = f  # Best feature value
                self.polarity = 1 if pos_seen > neg_seen else -1

            # Keep counts
            if label == 1:
                pos_seen += 1
                sum_pos_weights += w
            else:
                neg_seen += 1
                sum_neg_weights += w