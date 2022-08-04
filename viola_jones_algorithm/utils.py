import numpy as np
import os
import cv2
from features import HaarFeature, RectangleRegion, FeaturesTypes
import time


def to_integral(img: np.ndarray) -> np.ndarray:
    integral = np.cumsum(np.cumsum(img, axis=0), axis=1)
    return np.pad(integral, (1, 1), 'constant', constant_values=(0, 0))[:-1, :-1]

def summed_area(int_img, x1, y1, x2, y2):
    A = int_img[y1-1][x1-1]
    B = int_img[y1-1][x2]
    C = int_img[y2][x1-1]
    D = int_img[y2][x2]
    return A + D - C - B

def load_dataset(train_faces, train_non_faces):

    X = []
    y = []

    for file in os.listdir(train_faces):
        X.append(cv2.imread(train_faces + '/' +file, cv2.IMREAD_GRAYSCALE))
        y.append(1)

    for file in os.listdir(train_non_faces):
        X.append(cv2.imread(train_non_faces + '/' + file, cv2.IMREAD_GRAYSCALE))
        y.append(0)
    return X, y

def build_features(img_w, img_h, shift=1, min_w=4, min_h=4):

    features = []

    for w_width in range(min_w, img_w + 1):
        for w_height in range(min_h, img_h + 1):
            x = 1
            while x + w_width < img_w:
                y = 1
                while y + w_height < img_h:
                    if (w_width % 2 == 0):
                        features.append(HaarFeature(x, y, w_width, w_height, FeaturesTypes.EDGE_VERTICAL))
                    if (w_width % 3 == 0):
                        features.append(HaarFeature(x, y, w_width, w_height, FeaturesTypes.LINE_VERTICAL))
                    if (w_height % 2 == 0):
                        features.append(HaarFeature(x, y, w_width, w_height, FeaturesTypes.EDGE_HORIZONTAL))
                    if (w_height % 3 == 0):
                        features.append(HaarFeature(x, y, w_width, w_height, FeaturesTypes.LINE_HORIZONTAL))
                    if (w_height % 2 == 0 and w_width % 2 == 0):
                        features.append(HaarFeature(x, y, w_width, w_height, FeaturesTypes.SQUARED))
                    y = y + 1
                x = x + 1

    return np.array(features)


def apply_features(ii_array, features):
    X = np.zeros((len(features), len(ii_array)), dtype=np.int32)
    for i, feature in enumerate(features):
        X[i] = list(map(lambda ii: feature.compute_value(ii), ii_array))
    return np.array(X)

def get_pretty_time(start_time, end_time=None, s="", divisor=1.0):
    if not end_time:
        end_time = time.time()
    hours, rem = divmod((end_time - start_time)/divisor, 3600)
    minutes, seconds = divmod(rem, 60)
    return "{}{:0>2}:{:0>2}:{:05.8f}".format(s, int(hours), int(minutes), seconds)