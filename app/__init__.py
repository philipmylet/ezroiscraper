from flask import Flask
from .celery_app import make_celery
from .routes import bp

def create_app():
    app = Flask(__name__)
    app.config.update(
        CELERY_BROKER_URL='redis://redis:6379/0',
        CELERY_RESULT_BACKEND='redis://redis:6379/0'
    )
    
    app.celery = make_celery(app)
    app.register_blueprint(bp)
    
    return app

app = create_app()