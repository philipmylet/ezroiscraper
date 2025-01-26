from .celery_app import celery
import logging

@celery.task
def test_task():
    return "Task completed successfully!"

@celery.task(queue='default')
def scrape_data(user_id, batch_id, keyword, state):
    logging.info(f"Scrape task started: user={user_id}, batch={batch_id}")
    print(f"Scraping: user={user_id}, batch={batch_id}, keyword={keyword}, state={state}")
    return "Scraping completed"