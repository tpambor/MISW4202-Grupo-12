import os
from flask import Flask, request
from flask.views import MethodView
from flask_smorest import Api, Blueprint, abort
from marshmallow import Schema, fields
import requests

URL_AUTORIZADOR = os.getenv('AUTORIZADOR') or 'http://localhost:5001'
URL_ADMINCONTRATO = os.getenv('ADMINCONTRATO') or 'http://localhost:5002'

class ApiGateway(Api):
    DEFAULT_ERROR_RESPONSE_NAME = None

class LoginSchema(Schema):
    usuario = fields.String()

class LoginResponseSchema(Schema):
    token = fields.String()

blp = Blueprint("API Gateway", __name__)

@blp.route("/login")
class VistaLogin(MethodView):
    @blp.arguments(LoginSchema())
    @blp.response(200, LoginResponseSchema(), description="Iniciar sesión")
    def post(self, login):
        resLogin = requests.post(URL_AUTORIZADOR + "/login", json={'usuario': login['usuario']})
        if resLogin.status_code == 200:
            return {
                'token': resLogin.json()['token']
            }
        else:
            abort(resLogin.status_code, message=resLogin.json)

@blp.route("/contrato/<int:id_contrato>")
class VistaContrato(MethodView):
    @blp.response(200)
    def put(self, id_contrato):
        auth_header = request.headers.get('Authorization', '')
        headers = {'Authorization': auth_header}

        resValidate = requests.get(URL_AUTORIZADOR + "/validate", headers=headers)
        if resValidate.status_code == 200:
            resContrato = requests.put(f"{URL_ADMINCONTRATO}/contrato/{id_contrato}", headers=headers, json=request.json)
            if resContrato.status_code == 200:
                return resContrato.json()
            else:
                abort(resContrato.status_code, message=resContrato.json())
        else:
            abort(resValidate.status_code, message=resValidate.json())

app = Flask(__name__) 
app.config['API_TITLE'] = 'API Gateway'
app.config['API_VERSION'] = 'v1'
app.config['OPENAPI_VERSION'] = '3.1.0'
app.config['OPENAPI_URL_PREFIX'] = '/'
app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/' 

api = ApiGateway(app)
api.register_blueprint(blp)
