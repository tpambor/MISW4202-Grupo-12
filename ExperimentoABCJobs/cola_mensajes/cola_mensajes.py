from celery import Celery
from celery.signals import task_postrun

celery_app = Celery(__name__, broker='redis://localhost:6379/0')

@celery_app.task(name='search_best_candidates')
def search__best_candidates(id_vacancy, vacancyjson):
     pass

@task_postrun.connect()
def close_session(*args, **kwargs):
     pass
