import csv

import cv2
import os
from haar import Haar

data_eval = 1

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if(data_eval != 0):
        dataset = []
        directory = 'dataset/face_test'
        for filename in os.listdir(directory):
            if filename.endswith('.bmp'):
                image = cv2.imread(directory + '/' + filename)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                int_img = gray.cumsum(axis=0).cumsum(axis=1)
                haar = Haar(int_img)
                haar_features = haar.calculate_haar_features(int_img)
                dataset.append((haar_features, 1))
        directory = 'dataset/non_face_test'
        for filename in os.listdir(directory):
            if filename.endswith('.bmp'):
                image = cv2.imread(directory + '/' + filename)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                int_img = gray.cumsum(axis=0).cumsum(axis=1)
                haar = Haar(int_img)
                haar_features = haar.calculate_haar_features(int_img)
                dataset.append((haar_features, -1))

