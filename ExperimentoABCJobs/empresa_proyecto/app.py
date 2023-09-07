
from empresa_proyecto import create_app
from celery import Celery
from empresa_proyecto.tasks import celery_app


app = create_app('default')
app_context = app.app_context()
app_context.push()



@celery_app.task(name="request_best_candidates", queue="request")
def request_best_candidates(id_vacancy):
    pass

def publish_message(index):
    print('Enviando petición para calcular los mejores candidatos para la vacante ', index)
    args = (index,)
    request_best_candidates.apply_async(args=args, queue="request")

for index in range(1, 5):
    publish_message(index)

