from celery import Celery
from kombu import Exchange, Queue
import requests
import csv

celery_app = Celery(__name__, broker="redis://localhost:6379/0")
celery_app.conf.task_queues = (
    Queue('request', Exchange('request'), routing_key='best_candidates'),
)

nombre_archivo = "errores_detectados.csv"

def compare_and_save(responses, id_vacancy):

    # Todos los valores son iguales
    if responses[0] == responses[1] == responses[2]:   
        return responses[0]
    
    # Todos los valores son diferentes:
    # - Se devuelve un mensaje de error
    # - Se agregan todas las instancias como errores detectados
    elif len(responses) == len(set(responses)):
        for index in range(1, 4):
            nuevo_error = {
                "id_vacante": id_vacancy,
                "candidato_erroneo": responses[index - 1],
                "instancia": "motor_emparejamiento_" + str(index)
            }

            with open(nombre_archivo, "a+", newline='') as archivo_csv:
                fieldnames = ['id_vacante', "candidato_erroneo", 'instancia']

                # Crear el escritor CSV
                csv_writer = csv.DictWriter(archivo_csv, fieldnames=fieldnames)

                # Si el archivo está vacío, escribir la cabecera
                if archivo_csv.tell() == 0:
                    csv_writer.writeheader()

                # Escribir el registro
                csv_writer.writerow(nuevo_error)

        return 'No se pudo determinar el mejor candidato'
    
    # Solo un valor es diferente:
    # - Se devuelve el valor mayoritario
    # - Se agregala instancia respectiva como un error detectado
    else:
        most_common = None
        instance = None
        error_name = None

        if responses[0] == responses[1] != responses[2]:
            instance = '3'
            most_common = responses[0]
            error_name = responses[2]

        if responses[0] == responses[2] != responses[1]:
            instance = '2'
            most_common = responses[0]
            error_name = responses[1]
            
        if responses[1] == responses[2] != responses[0]:
            instance = '1'
            most_common = responses[1]
            error_name = responses[0]

        nuevo_error = {
            "id_vacante": id_vacancy,
            "candidato_erroneo": error_name,
            "instancia": "motor_emparejamiento_" + instance
        }

        with open(nombre_archivo, "a+", newline='') as archivo_csv:
            fieldnames = ['id_vacante', 'candidato_erroneo', 'instancia']

            # Crear el escritor CSV
            csv_writer = csv.DictWriter(archivo_csv, fieldnames=fieldnames)

            # Si el archivo está vacío, escribir la cabecera
            if archivo_csv.tell() == 0:
                csv_writer.writeheader()

            # Escribir el registro
            csv_writer.writerow(nuevo_error)

        return most_common


   
@celery_app.task(name="request.best_candidates")
def request_best_candidates(id_vacancy):
    print('Se empieza el calculo para la vacante {}'.format(id_vacancy))
    response_instance_1 = requests.get('http://127.0.0.1:5000/candidato/{}'.format(id_vacancy)).json()
    response_instance_2 = requests.get('http://127.0.0.1:5000/candidato/{}'.format(id_vacancy)).json()
    response_instance_3 = requests.get('http://127.0.0.1:5000/candidato/{}'.format(id_vacancy)).json()
    # response_instance_1 = {
    #     'nombre': 'Maria'
    # }
    # response_instance_2 = {
    #     'nombre': 'Pepe'
    # }
    # response_instance_3 = {
    #     'nombre': 'Pepe'
    # }
    final_candidate = compare_and_save([response_instance_1['nombre'], response_instance_2['nombre'], response_instance_3['nombre']], id_vacancy)
    args = (id_vacancy, final_candidate)
    print('Se envia el resultado para la vacante {}'.format(id_vacancy) )
    celery_app.send_task("response.best_candidates", args=args, queue="response")



