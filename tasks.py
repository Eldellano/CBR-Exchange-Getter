from celery_config import app
from exchange_get_save import logic


@app.task()
def run_exchange_get():
    return logic()
