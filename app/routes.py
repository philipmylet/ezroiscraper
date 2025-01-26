from flask import Blueprint, jsonify
from .tasks import test_task

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    task = test_task.delay()
    return jsonify({"task_id": task.id})