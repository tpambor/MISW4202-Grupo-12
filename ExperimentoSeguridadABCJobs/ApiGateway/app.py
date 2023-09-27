from flask_restful import Resource, Api
from flask import Flask, request
import requests


app = Flask(__name__)  
app_context = app.app_context()
app_context.push()

api = Api(app)

class VistaLogin(Resource):
    def post(self):
        resLogin = requests.post("http://127.0.0.1:5001/login", json={'usuario': request.json["usuario"]})
        return resLogin.json(), resLogin.status_code
    
class VistaContrato(Resource):
    def put(self, id_contrato):
        auth_header = request.headers.get('Authorization', '')
        headers = {'Authorization': auth_header}

        resValidate = requests.get("http://127.0.0.1:5001/validate", headers=headers)
        if resValidate.status_code == 200:
            resContrato = requests.put("http://127.0.0.1:5002/contrato/{}".format(id_contrato), headers=headers, json=request.json)
            return resContrato.json(), resContrato.status_code
        else:
            return resValidate.json(), resValidate.status_code

api.add_resource(VistaLogin, "/login")
api.add_resource(VistaContrato, "/contrato/<int:id_contrato>")
