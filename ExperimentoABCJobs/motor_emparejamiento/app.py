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
    def get(self, id_vacante):
        
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

        print("Llega petición para vacante ", id_vacante, " nombre ", name)

        # Log
        logging_data = {
            'id_vacante': id_vacante,
            'nombre': name,
            'instancia': INSTANCE_NAME
        }

        nombre_archivo = '{}.txt'.format(INSTANCE_NAME)

        if veridity == False:
            with open(nombre_archivo, "a+") as archivo:
                json.dump(logging_data, archivo)
                archivo.write('\n')


        # Retorno de respuesta
        return response, 200


# Agregar recurso a la API
api.add_resource(VistaCandidato, '/candidato/<int:id_vacante>')
