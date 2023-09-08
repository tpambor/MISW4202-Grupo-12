import threading
from celery import Celery
from kombu import Exchange, Queue
from time import sleep 

celery_app = Celery(__name__, broker="redis://localhost:6379/0")
celery_app.conf.task_queues = (
    Queue('response', Exchange('response'), routing_key='best_candidates'),
)

nombre_archivo = "mejores_candidatos.txt"

# class WorkerThread(object):
#     def __init__(self, celery_app):
#         self.celery_app = celery_app
#         self.worker = self.celery_app.Worker()
#         self.thread = threading.Thread(target=self.run, args=())
#         self.thread.daemon = True
#         self.thread.start()

#     def run(self):
#         self.worker.start()

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
        sleep(1)  

if __name__ == "__main__":
    # WorkerThread(celery_app)
    num_messages = 10  
    publish_messages(num_messages)
