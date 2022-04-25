from flask_restful import Resource
from flask import request, send_file
import cv2
import numpy


class User(Resource):

    def post(self):
        success = False
        data = request.form.to_dict()
        req = request
        check = None
        if 'file' in request.files:
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            filestr = request.files['file'].read()
            # convert string data to numpy array
            npimg = numpy.fromstring(filestr, numpy.uint8)
            # convert numpy array to image
            img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
            faces = face_cascade.detectMultiScale(img, 1.1, 4)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
            success = faces.shape[0]
            cv2.imwrite('testfile.jpg', img)

            check = True
        return True

    def get(self):
        print('test')
        return 'TEST'
