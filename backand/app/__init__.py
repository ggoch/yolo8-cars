from flask import Flask
from flask_restplus import Api

def create_app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='Machine Learning Model API',
              description='A simple API for a machine learning model')

    from .controllers.predict_controller import api as predict_ns
    api.add_namespace(predict_ns, path='/predict')

    return app