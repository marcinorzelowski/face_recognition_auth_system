from flask_restful import Resource
from flask import request, send_file
import cv2
import numpy


class Test(Resource):

    def get(self):
        return "TEST"
