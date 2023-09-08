from motor_emparejamiento import create_app
from flask_restful import Api, Resource
from faker import Faker
import csv


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
        if random < 90:
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
            'candidato_erroneo': name,
            'instancia': INSTANCE_NAME
        }

        nombre_archivo = '{}.csv'.format(INSTANCE_NAME)

        if veridity == False:
            with open(nombre_archivo, "a+", newline='') as archivo_csv:
                fieldnames = ['id_vacante', 'candidato_erroneo', 'instancia']

                # Crear el escritor CSV
                csv_writer = csv.DictWriter(archivo_csv, fieldnames=fieldnames)

                # Si el archivo está vacío, escribir la cabecera
                if archivo_csv.tell() == 0:
                    csv_writer.writeheader()

                # Escribir el registro
                csv_writer.writerow(logging_data)


        # Retorno de respuesta
        return response, 200


# Agregar recurso a la API
api.add_resource(VistaCandidato, '/candidato/<int:id_vacante>')
