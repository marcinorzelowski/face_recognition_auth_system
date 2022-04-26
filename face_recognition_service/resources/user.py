from flask_restful import Resource
from flask import request, send_file
import cv2
import numpy


class User(Resource):

    def post(self):
        data = request.form.to_dict()
        username = data['username']
        #TODO: Find in database user with such id
        if 'file' in request.files:
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            filestr = request.files['file'].read()
            npimg = numpy.fromstring(filestr, numpy.uint8)
            img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
            faces = face_cascade.detectMultiScale(img, 1.1, 4)
            if (len(faces) > 0):
                check = True
            else:
                check = False
            return check
