from flask_restplus import Namespace, Resource, fields
from flask import request
from ..models.model import load_model
from ..services.prediction_service import predict
from ..dtos.prediction_schema import get_prediction_model
from PIL import Image
import io

api = Namespace('prediction', description='Prediction operations')

upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type='file', required=True, help='The image file to upload')

model = load_model()
prediction_model = get_prediction_model(api)

@api.route('/')
class Predict(Resource):
    @api.expect(upload_parser)
    @api.marshal_with(prediction_model)
    def post(self):
        args = upload_parser.parse_args()
        file = args['file']
        if file.filename == '':
            api.abort(400, 'No file provided')

        try:
            image = Image.open(io.BytesIO(file.read()))
            predictions = predict(image, model)
            return {'predictions': predictions}
        except Exception as e:
            api.abort(500, str(e))