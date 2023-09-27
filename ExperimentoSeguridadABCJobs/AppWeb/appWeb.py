import requests
import json
import os
import csv
from faker import Faker
import random

baseUrl = 'http://localhost:5000'
candidatos = [
    {'userId': 'candidato_1', 'contratoId': 1},
    {'userId': 'candidato_2', 'contratoId': 2},
    {'userId': 'candidato_3', 'contratoId': 3},
    {'userId': 'candidato_4', 'contratoId': 4}
]
empleados = [
    {'userId': 'empleado_1', 'contratoId': 1},
    {'userId': 'empleado_2', 'contratoId': 2},
    {'userId': 'empleado_3', 'contratoId': 3},
    {'userId': 'empleado_4', 'contratoId': 4}
]
user_token = None
faker = Faker()
num_ciclos = 1000000


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
    Caso 4: Acceso denegado - Token inválido - Candidato con contrato invalido
    Establece el escenario de prueba
    :return: caso de prueba (String)
    """
    caso = random.choices(['caso1', 'caso2', 'caso3', 'caso4'], weights=[0.4, 0.2, 0.2, 0.2])[0]
    return caso


def register_results() -> None:
    with open('appweb.csv', 'a+', newline='') as archivo_csv:
        fieldnames = ['userId', 'contratoId', 'intento_exitoso', 'operacion_exitosa', 'token_valido']
        writer = csv.DictWriter(archivo_csv, fieldnames=fieldnames)
        writer.writeheader()
        # Iniciar ciclos
        for ciclo in range(1, num_ciclos + 1):
            # Establecer el caso
            caso = establish_scenario()
            # TODO: Implementar casos basado en los ejemplos anteriores


def main():
    pass


if __name__ == '__main__':
    main()
