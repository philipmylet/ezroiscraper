from app.celery_app import make_celery
from flask import current_app

celery = make_celery(current_app)

@celery.task
def test_task():
    return "Task completed successfully!"