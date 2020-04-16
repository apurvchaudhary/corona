from celery import Celery
from corona_app.utils import update_data_state_district_wise, update_data_state_wise


app = Celery()

@app.task
def update_data():
    try:
        update_data_state_district_wise()
        update_data_state_wise()
    except Exception:
        pass
