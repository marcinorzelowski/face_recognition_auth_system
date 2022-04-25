import cv2
import numpy as np
import csv
import math


class Haar(object):
    def __init__(self, image):
        self.image = image
        self.frame_width = 19
        self.frame_offset = 8
        self.haar_window_initial = 3


    def calculate_haar_features(self, integral_image):
        height, width = integral_image.shape
        haar_features = []

        #Structure of CSV is:
        #Feature Type, y1, x1, y2, x2, haar_window_size, value

        for haar_window_size in range(self.haar_window_initial, self.frame_width // 2, 3):
            for h in range(0, height - self.frame_width+1, self.frame_offset):
                for w in range(0, width - self.frame_width+1, self.frame_offset):
                    for h_frame in range(h, h + self.frame_width - haar_window_size, 1):
                        for w_frame in range(w, w + self.frame_width - haar_window_size, 1):
                            x1 = w_frame
                            x2 = w_frame + haar_window_size - 1
                            y1 = h_frame
                            y2 = h_frame + haar_window_size - 1
                            haar_vert_horizontal = self.calculate_rectangle_horizontal_haar(integral_image, x1, y1, x2, y2)
                            haar_features.append([haar_vert_horizontal])
                            haar_vert_vertiacal = self.calculate_rectangle_vertical_haar(integral_image, x1, y1, x2, y2)
                            haar_features.append([haar_vert_vertiacal])
                            haar_square = self.calculate_square_haar(integral_image, y1, x1, y2, x2)
                            haar_features.append([haar_square])
        return haar_features

    def calculate_square_haar(self, integral_image, x1, y1, x2, y2):
        y1_small = math.ceil(y1 + ((y2 - y1) / 3))  # first black
        y2_small = math.floor(y1 + ((y2 - y1) / 3 * 2))  # last black
        x1_small = math.ceil(x1 + ((x2 - x1) / 3))  # first black
        x2_small = math.floor(x1 + ((x2 - x1) / 3 * 2))
        black = self.calculate_integral_image_region(integral_image, x1_small, y1_small, x2_small, y2_small)
        white = self.calculate_integral_image_region(integral_image, x1, y1, x2, y2) - black

        return black - white

    def calculate_rectangle_horizontal_haar(self, integral_image, x1, y1, x2, y2):
        y_whiteUpper = math.ceil(y1 + ((y2 - y1) / 3))  # first black
        y_whiteLower = math.floor(y1 + ((y2 - y1) / 3 * 2))  # last black

        white = self.calculate_integral_image_region(integral_image, x1, y1, x2,
                                                y_whiteUpper - 1) + self.calculate_integral_image_region(integral_image, x1,
                                                                                                    y_whiteLower + 1,
                                                                                                    x2, y2)
        black = self.calculate_integral_image_region(integral_image, x1, y_whiteUpper, x2, y_whiteLower)
        return black - white

    def calculate_rectangle_vertical_haar(self, integral_image, x1, y1, x2, y2):
        x_left = math.ceil(x1 + ((x2 - x1) / 3))  # first black
        x_right = math.floor(x1 + ((x2 - x1) / 3 * 2))
        white = self.calculate_integral_image_region(integral_image, x1, y1, x_left - 1,
                                                y2) + self.calculate_integral_image_region(integral_image, x_right + 1, y1,
                                                                                      x2, y2)
        black = self.calculate_integral_image_region(integral_image, x_left, y1, x_right, y2)
        return black - white

    def calculate_integral_image_region(self, integral_image, x1, y1, x2, y2):
        A = 0
        B = 0
        C = 0
        D = (int)(integral_image[y2][x2])
        if x1 > 0 and y1 > 0:
            A = (int)(integral_image[y1 - 1][x1 - 1])
        if x1 > 0:
            B = (int)(integral_image[y2][x1 - 1])
        if y1 > 0:
            C = (int)(integral_image[y1 - 1][x2])
        return int(A - B - C + D)
