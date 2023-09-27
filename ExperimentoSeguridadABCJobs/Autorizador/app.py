from flask import Flask
from flask.views import MethodView
from flask_smorest import Api, Blueprint
from marshmallow import Schema, fields

class AutorizadorApi(Api):
    DEFAULT_ERROR_RESPONSE_NAME = None

class LoginSchema(Schema):
    usuario = fields.String()

class LoginResponseSchema(Schema):
    token = fields.String()

blp = Blueprint("Autorizacion", __name__, description="API para autorizar peticiones de usuarios")

@blp.route("/login")
class VistaLogin(MethodView):
    @blp.arguments(LoginSchema())
    @blp.response(200, LoginResponseSchema(), description="Iniciar sesión")
    def post(self, login):
        return {
            'token': 'abc'
        }

@blp.route("/validate")
class VistaValidate(MethodView):
    @blp.response(200, None)
    def get(self):
        pass

app = Flask(__name__)
app.config['API_TITLE'] = 'Autorizador API'
app.config['API_VERSION'] = 'v1'
app.config['OPENAPI_VERSION'] = '3.1.0'
app.config['OPENAPI_URL_PREFIX'] = '/'
app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

api = AutorizadorApi(app)
api.register_blueprint(blp)
