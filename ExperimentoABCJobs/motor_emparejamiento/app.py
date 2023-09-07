from motor_emparejamiento import create_app
from flask_restful import Api, Resource
import json
from faker import Faker


# Configuración de la App
app = create_app('default')
faker = Faker()
INSTANCE_NAME = 'motor_emparejamiento_1'

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

        # Escribir los datos de registro en un archivo de texto
        with open('logs/{}.txt'.format(INSTANCE_NAME), 'a') as file:
            file.write(json.dumps(logging_data) + '\n')


        # Retorno de respuesta
        return response, 200


# Agregar recurso a la API
api.add_resource(VistaCandidato, '/candidato')
