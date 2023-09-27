from flask import Flask
from flask.views import MethodView
from flask_smorest import Api, Blueprint, abort
from flask_jwt_extended import JWTManager, jwt_required, get_jwt
from marshmallow import Schema, fields

JWT_PUBLIC_KEY = (
    "-----BEGIN PUBLIC KEY-----\n"
    "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE+nGNooPLSTnPcXHGwEp8Igz5cuCl\n"
    "Wew8RPmYwxwqiAlAemdK8v0r3Z8IOWVq8289nlXXcN5OsLyoFxGo568XtQ==\n"
    "-----END PUBLIC KEY-----"
)

class ContratoSchema(Schema):
    terminos = fields.String()

# Diccionario de datos con contratos y usuarios
contratos = [
    {"contratoId": 1, "userId": "empleado_1"},
    {"contratoId": 1, "userId": "aspirante_1"},
    {"contratoId": 2, "userId": "empleado_2"},
    {"contratoId": 2, "userId": "aspirante_2"},
    {"contratoId": 3, "userId": "empleado_3"},
    {"contratoId": 3, "userId": "aspirante_3"},
    {"contratoId": 4, "userId": "empleado_4"},
    {"contratoId": 4, "userId": "aspirante_4"},
]

class AdminContratoApi(Api):
    DEFAULT_ERROR_RESPONSE_NAME = None

blp = Blueprint("Contratos", __name__, description="API para gestionar contratos")

@blp.route('/contrato/<int:contrato_id>')
class VistaContrato(MethodView):
    @jwt_required()
    @blp.arguments(ContratoSchema())
    @blp.response(200)
    def put(self, nuevo_contrato, contrato_id):
        contrato = next((c for c in contratos if c['contratoId'] == contrato_id), None)

        if contrato is None:
            abort(404, message='Contrato no encontrado')

        token = get_jwt()
        usuario = token['sub']
        print("usuario:", usuario)

        if not usuario.startswith("empleado_"):
            abort(403, message="El usuario no es un empleado")

        print(contrato['contratoId'])
        print(usuario[len("empleado_")])
        if str(contrato['contratoId']) == usuario[len("empleado_"):]:
            return {
                "mensaje": f"El contrato {contrato_id} pertenece al usuario {contrato['userId']}"
            }
        else:
            abort(403, message="El contrato no pertenece al usuario especificado")

app = Flask(__name__)
app.config['API_TITLE'] = 'AdminContrato API'
app.config['API_VERSION'] = 'v1'
app.config['JWT_ALGORITHM'] = 'ES256'
app.config['JWT_PUBLIC_KEY'] = JWT_PUBLIC_KEY
app.config['OPENAPI_VERSION'] = '3.1.0'
app.config['OPENAPI_URL_PREFIX'] = '/'
app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

jwt = JWTManager(app)

api = AdminContratoApi(app)
api.register_blueprint(blp)
