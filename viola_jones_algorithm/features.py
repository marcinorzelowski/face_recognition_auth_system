import numpy as np

import utils
from enum import Enum

class FeaturesTypes(Enum):
    EDGE_HORIZONTAL = 1,
    EDGE_VERTICAL = 2,
    LINE_VERTICAL = 3,
    LINE_HORIZONTAL = 4,
    SQUARED = 5


class RectangleRegion:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def compute_area_region(self, int_img):

        return utils.summed_area(int_img, self.x, self.y, self.x + self.width - 1, self.y + self.height - 1)

class HaarFeature:
    def __init__(self, x, y, width, height, type):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = type

    def __str__(self):
        return "(x= %d, y= %d, width= %d, height= %d, type= %s)" % (self.x, self.y, self.width, self.height, self.type)

    def __repr__(self):
        return "RectangleRegion(%d, %d, %d, %d)" % (self.x, self.y, self.width, self.height)

    def compute_value(self, int_img):
        white, black = 0, 0
        if self.type == FeaturesTypes.EDGE_VERTICAL:
            white = RectangleRegion(x= self.x, y=self.y, width=int(self.width/2), height=self.height).compute_area_region(int_img)
            black = RectangleRegion(x=self.x + int(self.width/2), y=self.y, width=int(self.width/2), height=self.height).compute_area_region(int_img)
        elif self.type == FeaturesTypes.EDGE_HORIZONTAL:
            white = RectangleRegion(x=self.x, y=self.y, width=self.width, height=int(self.height/2)).compute_area_region(int_img)
            black = RectangleRegion(x=self.x, y=self.y + int(self.height/2), width=int(self.width), height=int(self.height/2)).compute_area_region(int_img)
        elif self.type == FeaturesTypes.LINE_VERTICAL:
            white = RectangleRegion(x=self.x, y=self.y, width=int(self.width/3), height=self.height).compute_area_region(int_img) + RectangleRegion(x=int(self.x + 2*self.width/3), y=self.y, width=int(self.width/3), height=self.height).compute_area_region(int_img)
            black = RectangleRegion(x=self.x + int(self.width/3), y=self.y, width=int(self.width/3), height=self.height).compute_area_region(int_img)
        elif self.type == FeaturesTypes.LINE_HORIZONTAL:
            white = RectangleRegion(x=self.x, y=self.y, width=self.width, height=int(self.height/3)).compute_area_region(int_img) + RectangleRegion(x=self.x, y=int(self.y + 2*self.height/3), width=self.width, height=int(self.height/3)).compute_area_region(int_img)
            black = RectangleRegion(x=self.x, y=self.y + int(self.height/3), width=self.width, height=int(self.height/3)).compute_area_region(int_img)
        elif self.type == FeaturesTypes.SQUARED:
            white = RectangleRegion(x=self.x, y=self.y, width=int(self.width/2), height=int(self.height/2)).compute_area_region(int_img) + RectangleRegion(x=int(self.x + self.width/2), y=int(self.y + self.height/2), width=int(self.width/2), height=int(self.height/2)).compute_area_region(int_img)
            black = RectangleRegion(x=int(self.x + self.width/2), y=self.y, width=int(self.width/2), height=int(self.height/2)).compute_area_region(int_img) + RectangleRegion(x=self.x, y=int(self.y + self.height/2), width=int(self.width/2), height=int(self.height/2)).compute_area_region(int_img)
        return int(white) - int(black)