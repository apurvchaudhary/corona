from celery import Celery
from corona_app.utils import update_data_state_district_wise, update_data_state_wise

app = Celery()


@app.task
def update_data():
    """
    update data celery task calls two methods in utils
    update_data_state_district_wise - update district data(fields of model) of states
    update_data_state_wise - update country & state data(fields of model)
    """
    try:
        update_data_state_district_wise()
        update_data_state_wise()
    except Exception:
        pass
