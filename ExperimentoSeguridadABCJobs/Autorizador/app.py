from flask import Flask
from flask.views import MethodView
from flask_smorest import Api, Blueprint
from flask_jwt_extended import JWTManager, create_access_token
from marshmallow import Schema, fields

JWT_PRIVATE_KEY = (
    "-----BEGIN EC PRIVATE KEY-----\n"
    "MHcCAQEEIHXGfqltDuHbY1ARv0ilGSSqAIFMmbSrMzKhjkBbMZzyoAoGCCqGSM49\n"
    "AwEHoUQDQgAE+nGNooPLSTnPcXHGwEp8Igz5cuClWew8RPmYwxwqiAlAemdK8v0r\n"
    "3Z8IOWVq8289nlXXcN5OsLyoFxGo568XtQ==\n"
    "-----END EC PRIVATE KEY-----"
)

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
        access_token = create_access_token(identity=login['usuario'])
        return {
            'token': access_token
        }

@blp.route("/validate")
class VistaValidate(MethodView):
    @blp.response(200, None)
    def get(self):
        pass

app = Flask(__name__)
app.config['API_TITLE'] = 'Autorizador API'
app.config['API_VERSION'] = 'v1'
app.config['JWT_ALGORITHM'] = 'ES256'
app.config['JWT_PRIVATE_KEY'] = JWT_PRIVATE_KEY
app.config['OPENAPI_VERSION'] = '3.1.0'
app.config['OPENAPI_URL_PREFIX'] = '/'
app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

jwt = JWTManager(app)

api = AutorizadorApi(app)
api.register_blueprint(blp)
