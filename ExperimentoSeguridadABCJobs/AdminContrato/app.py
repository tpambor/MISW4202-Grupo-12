from flask_restful import  Api
from flask import Flask, request, jsonify
import re
import jwt

app = Flask(__name__)  
app_context = app.app_context()
app_context.push()

api = Api(app)

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

clave_secreta = "secret"

@app.route('/contrato/<int:contrato_id>', methods=['PUT'])
def editar_contrato(contrato_id):
    contrato = next((c for c in contratos if c['contratoId'] == contrato_id), None)
    
    if contrato is None:
        return jsonify({"error": "Contrato no encontrado"}), 404
    
    tokenRequest = request.json["token"]
    token = tokenRequest.get(token)
    
    try:
    # Verificar y decodificar el token
        payload = jwt.decode(token, clave_secreta, algorithms=["HS256"])
        usuario = payload.get('usuario')
        print("usuario:", usuario)
    except jwt.InvalidTokenError:
        print("El token no es válido.")
        
    if not usuario.startswith("empleado_"):
        return jsonify({"error": "El usuario no es un empleado"}), 403
    
    print(contrato['contratoId'])
    print(usuario[len("empleado_")])
    if str(contrato['contratoId']) ==  usuario[len("empleado_"):]:
        return jsonify({"mensaje": f"El contrato {contrato_id} pertenece al usuario { contrato['userId']}"}), 200
    else:
        return jsonify({"error": "El contrato no pertenece al usuario especificado"}), 403


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)