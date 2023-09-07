from celery import Celery
from celery.signals import task_postrun
import requests
import json

celery_app = Celery(__name__, broker='redis://localhost:6379/0')
     
@celery_app.task(name='search_best_candidates')
def search_best_candidates(id_vacancy):
    send_to_voting(id_vacancy)

def send_to_voting(id_vacancy):
    voting_url = "http://localhost:5000/voting" 

    data = {
        "id_vacancy": id_vacancy
    }

    try:
        response = requests.post(voting_url, json=data)

        if response.status_code == 200:
            print(f"Solicitud enviada a Voting {id_vacancy}")
        else:
            print(f"Error al enviar la solicitud a Voting: {response.status_code}")
    except Exception as e:
        print(f"Error al enviar la solicitud a Voting: {str(e)}")


@task_postrun.connect()
def close_session(*args, **kwargs):
    pass
