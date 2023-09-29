from flask import Flask
from flask.views import MethodView
from flask_smorest import Api, Blueprint, abort
from flask_jwt_extended import JWTManager, create_access_token, get_jwt, verify_jwt_in_request
from marshmallow import Schema, fields

JWT_PUBLIC_KEY = (
    "-----BEGIN PUBLIC KEY-----\n"
    "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE+nGNooPLSTnPcXHGwEp8Igz5cuCl\n"
    "Wew8RPmYwxwqiAlAemdK8v0r3Z8IOWVq8289nlXXcN5OsLyoFxGo568XtQ==\n"
    "-----END PUBLIC KEY-----"
)

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
        additional_claims = dict()
        # Authentication no es el punto de sensibilidad del experimento
        # Vamos a asumir que cada usuario es valido y que los usuarios que empiezan con empleado_ pertecen al rol de empleado
        if login['usuario'].startswith('empleado_'):
            additional_claims['rol'] = 'empleado'
        else:
            additional_claims['rol'] = 'aspirante'

        access_token = create_access_token(identity=login['usuario'], additional_claims=additional_claims)
        return {
            'token': access_token
        }

@blp.route("/validate/contrato/editar")
class VistaValidate(MethodView):
    @blp.response(200, None)
    def get(self):
        try:
            verify_jwt_in_request()
        except:
            print("Token invalido", flush=True)
            abort(403, message="Token invalido")

        token = get_jwt()
        # Verificar si el usuario es autorizado para editar un contrato
        if token['rol'] != 'empleado':
            print("Solo empleados pueden editar un contrato", flush=True)
            abort(403, message="Solo empleados pueden editar un contrato")

app = Flask(__name__)
app.config['API_TITLE'] = 'Autorizador API'
app.config['API_VERSION'] = 'v1'
app.config['JWT_ALGORITHM'] = 'ES256'
app.config['JWT_PUBLIC_KEY'] = JWT_PUBLIC_KEY
app.config['JWT_PRIVATE_KEY'] = JWT_PRIVATE_KEY
app.config['OPENAPI_VERSION'] = '3.1.0'
app.config['OPENAPI_URL_PREFIX'] = '/'
app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

jwt = JWTManager(app)

api = AutorizadorApi(app)
api.register_blueprint(blp)
