from celery import Celery

celery_app = Celery(__name__, broker="redis://localhost:6379/0")


nombre_archivo = 'mejores_candidatos.txt'

@celery_app.task(name="response_best_candidates", queue="response")
def response_best_candidates(id_vacancy, final_candidate):
  print('Se recibe el resultado para la vacante {}'.format(id_vacancy))
  with open(nombre_archivo, "a+") as file:
    file.write('Para la vacante {} el mejor candidato es {} \n'.format(id_vacancy, final_candidate))
