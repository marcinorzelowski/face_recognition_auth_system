from flask import Flask
from flask_restful import Api

from resources.user import User
from resources.test import Test


app = Flask(__name__)

api = Api(app)

api.add_resource(User, '/user')
api.add_resource(Test, '/test')


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
