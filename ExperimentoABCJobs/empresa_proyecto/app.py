import threading
import csv
import os
from time import sleep 
from celery import Celery
from kombu import Exchange, Queue

NOMBRE_ARCHIVO = os.getenv('LOGFILE') or "mejores_candidatos.csv"
BROKER = os.getenv('BROKER') or "redis://localhost:6379/0"
NUM_MESSAGES = int(os.getenv('NUM_MESSAGES') or 1000)

celery_app = Celery(__name__, broker=BROKER)
celery_app.conf.task_queues = (
    Queue('response', Exchange('response'), routing_key='best_candidates'),
)


class WorkerThread(object):
    def __init__(self, celery_app):
        self.celery_app = celery_app
        self.worker = self.celery_app.Worker()
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True
        self.thread.start()

    def run(self):
        self.worker.start()


@celery_app.task(name="response.best_candidates")
def response_best_candidates(id_vacancy, final_candidate):
    print('El mejor candidato para la vacante {} es {}\n'.format(id_vacancy, final_candidate))
    response = {
        'id_vacante': id_vacancy,
        'mejor_candidato': final_candidate,
    }

    with open(NOMBRE_ARCHIVO, "a+", newline='') as archivo_csv:
        fieldnames = ['id_vacante', 'mejor_candidato']

        # Crear el escritor CSV
        csv_writer = csv.DictWriter(archivo_csv, fieldnames=fieldnames)

        # Si el archivo está vacío, escribir la cabecera
        if archivo_csv.tell() == 0:
            csv_writer.writeheader()

        # Escribir el registro
        csv_writer.writerow(response)

def publish_messages(num_messages):
    app = Celery(__name__, broker=BROKER)
    for index in range(1, num_messages + 1):
        args = (index,)
        app.send_task("request.best_candidates", args, queue="request")
        print(f"Enviada solicitud {index} a la cola de mensajes.")
        sleep(0.01)

if __name__ == "__main__":
    WorkerThread(celery_app)
    sleep(10)
    publish_messages(NUM_MESSAGES)
    sleep(10)
