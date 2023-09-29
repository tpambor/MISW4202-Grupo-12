import requests
import json
import os
import csv
from faker import Faker
import random

# URL del API Gateway
baseUrl = 'http://localhost:5000'

# Listas de diccionarios con usuarios empleados y candidatos
candidatos = [
    {'userId': 'aspirante_1', 'contratoId': 1},
    {'userId': 'aspirante_2', 'contratoId': 2},
    {'userId': 'aspirante_3', 'contratoId': 3},
    {'userId': 'aspirante_4', 'contratoId': 4}
]
empleados = [
    {'userId': 'empleado_1', 'contratoId': 1},
    {'userId': 'empleado_2', 'contratoId': 2},
    {'userId': 'empleado_3', 'contratoId': 3},
    {'userId': 'empleado_4', 'contratoId': 4}
]
faker = Faker()

# Numero de peticiones a realizar
num_ciclos = 5000


def make_login(usuario: dict) -> str or None:
    """
    Realiza el login de un usuario y obtiene el token de acceso
    :param usuario: diccionario con los datos del usuario (empleado o candidato)
    :return: Token de acceso (String) o None si el login falló
    """
    url = baseUrl + '/login'
    data = {'usuario': usuario['userId']}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        returned_token = response.json().get('token')
        return returned_token
    else:
        print('Error al hacer login')
        return None


def establish_scenario() -> str:
    """
    Caso 1: Operación exitosa - Token válido - Empleado con contrato valido
    Caso 2: Acceso denegado - Token inválido - Empleado con contrato valido
    Caso 3: Acceso denegado - Token válido - Empleado con contrato invalido
    Caso 4: Acceso denegado - Token válido - Candidato con contrato invalido
    Establece el escenario de prueba
    :return: caso de prueba (String)
    """
    caso = random.choices(['caso1', 'caso2', 'caso3', 'caso4'], weights=[0.4, 0.2, 0.2, 0.2])[0]
    return caso


def make_contract_request(user_data: dict, user_token: str, ciclo: int, caso: str,
                          valid_token: bool, valid_contract: bool) -> dict:
    """
    Realiza la solicitud de contrato
    :param valid_contract: Indica si el contrato es el correcto o no
    :param user_data: datos del usuario (empleado o candidato)
    :param user_token: token de acceso
    :param ciclo: ciclo actual
    :param caso: caso de prueba
    :param valid_token: indica si el token es válido o no
    :return: diccionario con los datos de la solicitud
    """

    # Validar caso
    if caso == 'caso1':
        success = True
    else:
        success = False

    # validar token
    if valid_token:
        token_valido = True
    else:
        token_valido = False

    # Validar contrato
    if not valid_contract:
        user_data['contratoId'] = faker.random_int(min=5, max=10)

    # Realizar la operación con el token obtenido
    url = f'{baseUrl}/contrato/{user_data["contratoId"]}'
    headers = {'Authorization': f'Bearer {user_token}'}
    data = {'terminos': 'ABC def Lorem ipsum'}
    response = requests.put(url, headers=headers, json=data)

    # Escribir los datos de registro en el archivo CSV
    logging_data = {
        'ciclo': ciclo,
        'userId': user_data['userId'],
        'contratoId': user_data['contratoId'],
        'intento_exitoso': success,
        'operacion_exitosa': response.status_code == 200,
        'token_valido': token_valido, 
        'caso': caso
    }
    return logging_data


def register_results() -> None:
    """
    Ejecuta el experimento y registra los resultados en un archivo CSV
    :return:
    """
    with open('appweb.csv', 'a+', newline='') as archivo_csv:
        fieldnames = ['ciclo', 'userId', 'contratoId', 'intento_exitoso', 'operacion_exitosa', 'token_valido', 'caso']
        writer = csv.DictWriter(archivo_csv, fieldnames=fieldnames)
        writer.writeheader()
        # Iniciar ciclos
        for ciclo in range(1, num_ciclos + 1):
            print(f'ciclo ', ciclo)
            # Establecer el caso
            caso = establish_scenario()

            if caso == 'caso1':
                user_data = random.choice(empleados).copy()
                user_token = make_login(user_data)
                if user_token:
                    # Realizar la operación con el token obtenido
                    valid_token = True
                    valid_contract = True
                    logging_data = make_contract_request(user_data, user_token, ciclo, caso, valid_token,
                                                         valid_contract)
                    writer.writerow(logging_data)

            elif caso == 'caso2':
                user_data = random.choice(empleados).copy()
                user_token = faker.sha256()
                # Realizar la operación con un código aleatorio en lugar del token
                valid_token = False
                valid_contract = True
                logging_data = make_contract_request(user_data, user_token, ciclo, caso, valid_token,
                                                     valid_contract)
                writer.writerow(logging_data)

            elif caso == 'caso3':
                user_data = random.choice(empleados).copy()
                user_token = make_login(user_data)
                if user_token:
                    # Realizar la operación con el token obtenido
                    valid_token = True
                    valid_contract = False
                    logging_data = make_contract_request(user_data, user_token, ciclo, caso, valid_token,
                                                         valid_contract)
                    writer.writerow(logging_data)

            elif caso == 'caso4':
                user_data = random.choice(candidatos).copy()
                user_token = make_login(user_data)
                if user_token:
                    # Realizar la operación con el token obtenido
                    valid_token = True
                    valid_contract = True
                    logging_data = make_contract_request(user_data, user_token, ciclo, caso, valid_token,
                                                         valid_contract)
                    writer.writerow(logging_data)


if __name__ == '__main__':
    register_results()
