import numpy as np

import utils
import time
from viola_jones import ViolaJones




train_faces = "./coding_set/faces"
train_non_faces = "./coding_set/non-faces"
test_faces = "./testset/faces"
test_non_faces = "./testset/non-faces"


def prepare_dataset(X, y):
    X, y = np.array(X), np.array(y)
    idx_shuffled = np.random.permutation(len(y))
    X = X[idx_shuffled]
    y = y[idx_shuffled]
    return X, y


def evaluate(clf, X, y):
    correct = 0
    all_negatives, all_positives = 0, 0
    true_negatives, false_negatives = 0, 0
    true_positives, false_positives = 0, 0
    classification_time = 0


    for x, label in zip(X, y):

        if label == 1:
            all_positives += 1
        else:
            all_negatives += 1

        start = time.time()

        prediction = clf.classify(x)
        classification_time += time.time() - start
        if prediction == 1 and label == 0:
            false_positives += 1
        if prediction == 0 and label == 1:
            false_negatives += 1

        correct += 1 if prediction == label else 0

    print("False Positive Rate: %d/%d (%f)" % (false_positives, all_negatives, false_positives / all_negatives))
    print("False Negative Rate: %d/%d (%f)" % (false_negatives, all_positives, false_negatives / all_positives))
    print("Accuracy: %d/%d (%f)" % (correct, len(X), correct / len(X)))
    print("Average Classification Time: %f" % (classification_time / len(X)))

if __name__ == "__main__":
    X, y = utils.load_dataset(train_faces, train_non_faces)
    pos_count = np.sum(y)
    neg_count = np.sum(len(y)-pos_count)
    X, y = prepare_dataset(X, y)
    clf = ViolaJones(layers=[1, 5])
    clf.train2(X, y)

    X, y = utils.load_dataset(test_faces, train_non_faces)
    evaluate(clf, X, y)





