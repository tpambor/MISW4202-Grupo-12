from flask import Flask
from flask.views import MethodView
from flask_smorest import Api, Blueprint

class AutorizadorApi(Api):
    DEFAULT_ERROR_RESPONSE_NAME = None

blp = Blueprint("Autorizacion", __name__, description="API para autorizar peticiones de usuarios")

@blp.route("/login")
class VistaLogin(MethodView):
    def post(self):
        pass

@blp.route("/validate")
class VistaValidate(MethodView):
    def post(self):
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
