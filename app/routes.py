from flask import Blueprint, jsonify, request
from .tasks import test_task
from celery.result import AsyncResult
from .celery_app import celery
from .tasks import scrape_data
from .utils import ensure_worker_running

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    task = test_task.delay()
    return jsonify({"task_id": task.id})

@bp.route('/status/<task_id>')
def task_status(task_id):
    task_result = AsyncResult(task_id)
    if task_result.state == 'PENDING':
        response = {
            'state': task_result.state,
            'status': 'Pending...'
        }
    elif task_result.state != 'FAILURE':
        response = {
            'state': task_result.state,
            'result': task_result.result
        }
    else:
        response = {
            'state': task_result.state,
            'status': str(task_result.result)
        }
    return jsonify(response)

@bp.route('/scrape', methods=['POST'])
def start_scraping():
    data = request.get_json()
    user_id = data.get('user_id')
    batch_id = data.get('batch_id')
    keyword = data.get('keyword')
    state = data.get('state')

    if not all([user_id, batch_id, keyword, state]):
        return jsonify({"error": "Missing required parameters"}), 400

    # Ensure worker is running
    if not ensure_worker_running(user_id):
        return jsonify({"error": "Failed to start worker"}), 500

    # Queue task on user-specific queue
    task = scrape_data.apply_async(
        args=[user_id, batch_id, keyword, state],
        queue=f'worker_user_{user_id}'
    )

    return jsonify({"task_id": task.id})