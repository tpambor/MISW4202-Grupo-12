from flask_restful import  Api
from flask import Flask, jsonify
import re

app = Flask(__name__)  
app_context = app.app_context()
app_context.push()

api = Api(app)

# Diccionario de datos con contratos y usuarios
contratos = [
    {"userId": "empleado_1", "contratoId": 1, "aspiranteId": 1},
    {"userId": "empleado_2", "contratoId": 2, "aspiranteId": 2},
    {"userId": "empleado_3", "contratoId": 3, "aspiranteId": 3},
    {"userId": "empleado_4", "contratoId": 4, "aspiranteId": 4},
]
    
@app.route('/contrato/<int:contrato_id>', methods=['PUT'])
def editar_contrato(contrato_id):
    contrato = next((c for c in contratos if c['contratoId'] == contrato_id), None)

    if contrato is None:
        return jsonify({"error": "Contrato no encontrado"}), 404

    numero = re.search(r'\d+', contrato['userId']).group()
    
    if  str(contrato['contratoId']) == numero:
        return jsonify({"mensaje": f"El contrato {contrato_id} pertenece al usuario {numero}"}), 200
    else:
        return jsonify({"error": "El contrato no pertenece al usuario especificado"}), 403

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)