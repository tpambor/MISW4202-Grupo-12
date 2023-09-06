from motor_emparejamiento import create_app
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import requests
import json
from faker import Faker
import logging

# Configuración de la App
app = create_app('default')
faker = Faker()
INSTANCE_NAME = 'motor_emparejamiento_1'
logging.basicConfig(
    filename='logs/{}.log'.format(INSTANCE_NAME),
    level=logging.INFO,
)

# Inicializar API
api = Api(app)

# Vista
counter = 0


class VistaCandidato(Resource):
    def get(self):
        global counter
        counter += 1

        # Valor random para generar dato veridico o no
        random = faker.random_int(min=0, max=100)

        # Generación de datos
        if random < 75:
            name = 'Don Octavio Mesa'
            veridity = True
        else:
            name = faker.name()
            veridity = False

        # Generación de respuesta
        response = {
            'nombre': name,
        }

        # Log
        logging_data = {
            'numero': counter,
            'nombre': name,
            'veracidad': veridity,
            'instancia': INSTANCE_NAME
        }
        logging.info(json.dumps(logging_data))

        # Retorno de respuesta
        return response, 200


# Agregar recurso a la API
api.add_resource(VistaCandidato, '/candidato')
