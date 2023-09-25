from flask import Flask
from flask_restful import Api, Resource
from faker import Faker
import csv
import os

NOMBRE_ARCHIVO = os.getenv('LOGFILE') or "motor_emparejamiento.csv"

# Configuración de la App
app = Flask(__name__)
faker = Faker()

# Inicializar API
api = Api(app)

# Vista
class VistaCandidato(Resource):
    def get(self, id_vacante):
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
            'candidato_erroneo': name
        }

        if veridity == False:
            with open(NOMBRE_ARCHIVO, "a+", newline='') as archivo_csv:
                fieldnames = ['id_vacante', 'candidato_erroneo']

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
