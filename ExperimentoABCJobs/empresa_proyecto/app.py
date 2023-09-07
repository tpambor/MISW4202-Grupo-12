
from empresa_proyecto import create_app
from celery import Celery

celery_app = Celery(__name__, broker="redis://localhost:6379/0")

app = create_app('default')
app_context = app.app_context()
app_context.push()

@celery_app.task(name="response_best_candidates")
def response_best_candidates(response):
   print(response)


@celery_app.task(name="registrar_log")
def registrar_log(id_vacancy, best_candidate):
    with open("log_signin.txt", "a+") as file:
        file.write("Para la vacante {}, el mejor candidato es: {}\n".format(id_vacancy, id_vacancy))

@celery_app.task(name="request_best_candidates")
def request_best_candidates(id_vacancy):
    pass

def publish_message(index):
    args = (index,)
    request_best_candidates.apply_async(args)

for index in range(1, 10):
    publish_message(index)

