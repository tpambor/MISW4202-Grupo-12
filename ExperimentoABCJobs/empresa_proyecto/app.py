
from empresa_proyecto import create_app
from celery import Celery
from cola_mensajes import search_best_candidates 
from time import sleep 


app = create_app('default')
app_context = app.app_context()
app_context.push()

@celery_app.task(name="response_best_candidates")
def response_best_candidates(response):\
   print(response)


@celery_app.task(name="request_best_candidates", queue="request")
def request_best_candidates(id_vacancy):
    search_best_candidates.apply_async(args=[id_vacancy])


def publish_messages(num_messages):
    for index in range(1, num_messages + 1):
        args = (index,)
        request_best_candidates.apply_async(args)
        print(f"Enviada solicitud {index} a la cola de mensajes.")
        sleep(1)  

if __name__ == "__main__":
    num_messages = 1000  
    publish_messages(num_messages)