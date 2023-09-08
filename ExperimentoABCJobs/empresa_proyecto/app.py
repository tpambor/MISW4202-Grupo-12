import threading
from celery import Celery
from kombu import Exchange, Queue
from time import sleep 

celery_app = Celery(__name__, broker="redis://localhost:6379/0")
celery_app.conf.task_queues = (
    Queue('response', Exchange('response'), routing_key='best_candidates'),
)

nombre_archivo = "mejores_candidatos.txt"


@celery_app.task(name="response.best_candidates")
def response_best_candidates(id_vacancy, final_candidate):
    with open(nombre_archivo, "a+") as file:
            file.write('El mejor candidato para la vacante {} es {}\n'.format(id_vacancy, final_candidate))

def publish_messages(num_messages):
    # app = Celery(__name__, broker="redis://localhost:6379/0")
    for index in range(1, num_messages + 1):
        args = (index,)
        celery_app.send_task("request.best_candidates", args, queue="request")
        print(f"Enviada solicitud {index} a la cola de mensajes.")

if __name__ == "__main__":
    num_messages = 100
    publish_messages(num_messages)
