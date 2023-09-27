import requests
import json
import os
import csv
from faker import Faker
import random

baseUrl = 'http://localhost:5000'
candidatos = [...]
empleados = [...]
user_token = None
faker = Faker()


def make_login(candidato: dict) -> str:
    # La función make_login() ya está definida como en la respuesta anterior
    pass


def main():
    with open('logging_data.csv', mode='w', newline='') as csv_file:
        fieldnames = ['userId', 'contratoId', 'intento_exitoso', 'operacion_exitosa', 'token_valido']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for _ in range(1000000):
            # Establecer el caso
            caso = random.choices(['caso1', 'caso2', 'caso3', 'caso4'], weights=[0.4, 0.2, 0.2, 0.2])[0]

            if caso == 'caso1':
                user_data = random.choice(empleados)
                token = make_login(user_data)
                if token:
                    # Realizar la operación con el token obtenido
                    url = f'{baseUrl}/contrato/{user_data["contratoId"]}'
                    data = {'token': token}
                    response = requests.put(url, json=data)

                    # Escribir los datos de registro en el archivo CSV
                    logging_data = {
                        'userId': user_data['userId'],
                        'contratoId': user_data['contratoId'],
                        'intento_exitoso': True,
                        'operacion_exitosa': response.status_code == 200,
                        'token_valido': True
                    }
                    writer.writerow(logging_data)

            elif caso == 'caso2':
                user_data = random.choice(empleados)
                codigo_aleatorio = faker.random_int(min=1000, max=9999)
                # Realizar la operación con un código aleatorio en lugar del token
                url = f'{baseUrl}/contrato/{user_data["contratoId"]}'
                data = {'token': codigo_aleatorio}
                response = requests.put(url, json=data)

                # Escribir los datos de registro en el archivo CSV
                logging_data = {
                    'userId': user_data['userId'],
                    'contratoId': user_data['contratoId'],
                    'intento_exitoso': False,
                    'operacion_exitosa': response.status_code == 200,
                    'token_valido': False
                }
                writer.writerow(logging_data)

            # Implementar casos 3 y 4 de manera similar


if __name__ == '__main__':
    main()
