from celery import Celery

def make_celery(app=None):
    celery = Celery(
        "celery_app",
        broker='redis://redis:6379/0',
        backend='redis://redis:6379/0'
    )

    if app:
        class ContextTask(celery.Task):
            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return self.run(*args, **kwargs)
        celery.Task = ContextTask

    return celery

celery = make_celery()