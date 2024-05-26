from flask_restplus import fields

def get_prediction_model(api):
    return api.model('Prediction', {
        'predictions': fields.List(fields.Float, description='Prediction results')
    })