from celery import Celery
import requests

from collections import Counter

celery_app = Celery(__name__, broker="redis://localhost:6379/0")

@celery_app.task(name="response_best_candidates")
def response_best_candidates(response):
   pass

nombre_archivo = "errores_detectados.txt"

def compare_and_save(responses, id_vacancy):
    errorDetectadoMsg = 'Error detectado en la instancia '

    # Todos los valores son iguales
    if responses[0] == responses[1] == responses[2]:   
        return responses[0]
    
    # Todos los valores son diferentes:
    # - Se devuelve un mensaje de error
    # - Se agregan todas las instancias como errores detectados
    elif responses[0] != responses[1] != responses[2]:
        for index in range(1, 4):
            with open(nombre_archivo, "a+") as file:
                file.write(errorDetectadoMsg + index + ' para la vacante ' + id_vacancy)
        return 'No se pudo determinar el mejor candidato'
    
    # Solo un valor es diferente:
    # - Se devuelve el valor mayoritario
    # - Se agregala instancia respectiva como un error detectado
    else:
        most_common
        instance

        if responses[0] == responses[1] != responses[2]:
            instance = '3'
            most_common = responses[0]

        if responses[0] == responses[2] != responses[1]:
            instance = '2'
            most_common = responses[0]
            
        if responses[1] == responses[2] != responses[0]:
            instance = '1'
            most_common = responses[1]

        with open(nombre_archivo, "a+") as file:
            file.write(errorDetectadoMsg + instance + ' para la vacante ' + id_vacancy)

        return most_common


   
@celery_app.task(name="request_best_candidates")
def request_best_candidates(id_vacancy):
#   response_instance_1 = requests.get('"http://monitor-1:5000')
#   response_instance_2 = requests.get('"http://monitor-2:5000')
#   response_instance_3 = requests.get('"http://monitor-3:5000')
    response_instance_1 = {
        'nombre': 'Pepe'
    }
    response_instance_2 = {
        'nombre': 'Pepe'
    }
    response_instance_3 = {
        'nombre': 'Jose'
    }
    final_candidate = compare_and_save([response_instance_1.nombre, response_instance_2.nombre, response_instance_3.nombre], id_vacancy)
    args = (id_vacancy, final_candidate)
    response_best_candidates.apply_async(args)



