from celery import Celery
import requests

from collections import Counter

def most_common_value(responses):
    contador = Counter(responses)
    
    most_common_val = contador.most_common(1)
    
    # Si todos los valores son diferentes, devuelve 'Ninguno'
    if len(most_common_val) == 0 or most_common_val[0][1] == 1:
        return 'No se pudo determinar el mejor candidato'
    
    return most_common_val[0][0]

celery_app = Celery(__name__, broker="redis://localhost:6379/0")

@celery_app.task(name="response_best_candidates")
def response_best_candidates(response):
   pass
   
@celery_app.task(name="request_best_candidates")
def request_best_candidates(id_vacancy):
  response_instance_1 = requests.get('"http://monitor-1:5000')
  response_instance_2 = requests.get('"http://monitor-2:5000')
  response_instance_3 = requests.get('"http://monitor-3:5000')
  final_candidate = most_common_value([response_instance_1.nombre, response_instance_2.nombre, response_instance_3.nombre])
  args = (id_vacancy, final_candidate)
  response_best_candidates.apply_async(args)



