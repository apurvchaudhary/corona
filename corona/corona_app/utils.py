import requests
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework.response import Response

from corona_app.models import State, Country, District
from rest_framework import status
from corona_app.serializers import StateSerializer, CountrySerializer
from corona_app.constants import UPDATE_COUNTRY_DATA_URL, UPDATE_STATE_DISTRICT_DATA_URL, INDIAN_STATES


def response(data, code=status.HTTP_200_OK):
    """
    Overrides rest_framework response
    :param data: data to be send in response
    :param code: response status code(default has been set to 200)
    :param error: error message(if any, not compulsory)
    """
    return Response(data=data, status=code)


def get_country_data(request):
    try:
        country = Country.objects.prefetch_related("state_set").filter(name='India').first()
    except ObjectDoesNotExist:
        return response(data="No country with this name", code=status.HTTP_404_NOT_FOUND)
    else:
        country_serializer = CountrySerializer(country)
        return render(request, template_name='home.html', context={'data': country_serializer.data})


def get_graph_data():
    labels = []
    data = []
    states = State.objects.order_by("patients").prefetch_related("district_set")
    serializer = StateSerializer(states, many=True)
    for state in serializer.data:
        labels.append(state["name"])
        data.append(state["patients"])
    return response(data={'labels': labels, 'data': data})


def get_state_data_by_name(request):
    state_id = request.query_params.get("state_id")
    if state_id:
        try:
            state = State.objects.prefetch_related("district_set").filter(id=state_id).first()
        except ObjectDoesNotExist:
            return response(data="No state with this name", code=status.HTTP_404_NOT_FOUND)
        else:
            state_serializer = StateSerializer(state)
            return render(request, template_name="state.html", context={"data": state_serializer.data})
    return response(data="No state id given", code=status.HTTP_400_BAD_REQUEST)


def get_state_graph_data(request):
    state_id = request.query_params.get("state_id")
    if state_id:
        try:
            state = State.objects.prefetch_related("district_set").filter(id=state_id).first()
        except ObjectDoesNotExist:
            return response(data="No state with this name", code=status.HTTP_404_NOT_FOUND)
        else:
            state_serializer = StateSerializer(state)
            if state_serializer:
                labels = []
                data = []
                for dist in state_serializer.data.get("district"):
                    labels.append(dist["name"])
                    data.append(dist["patients"])
                return response(data={'labels': labels, 'data': data})
    return response(data="No state id given", code=status.HTTP_400_BAD_REQUEST)


def update_data_state_wise():
    try:
        response_data = requests.get(UPDATE_COUNTRY_DATA_URL)
        data = response_data.json()
        active_now = data.get("statewise")[0].get("active")
        confirmed = data.get("statewise")[0].get("confirmed")
        death = data.get("statewise")[0].get("deaths")
        recovered = data.get("statewise")[0].get("recovered")
        delta_confirmed = data.get("statewise")[0].get("deltaconfirmed")
        delta_recovered = data.get("statewise")[0].get("deltarecovered")
        delta_death = data.get("statewise")[0].get("deltadeaths")
        country = Country.objects.get(name="India")
        if active_now and confirmed and death and recovered:
            country.death, country.recovered, country.patients, country.active_now, \
            country.delta_confirmed, country.delta_recovered, country.delta_death = \
                death, recovered, confirmed, active_now, delta_confirmed, delta_recovered, delta_death
            country.last_updated = datetime.now()
            country.save()
        for state in data.get("statewise")[1:]:
            state_obj = State.objects.filter(name=state.get("state")).first()
            if state_obj:
                state_obj.patients = state.get("confirmed")
                state_obj.death = state.get("deaths")
                state_obj.recovered = state.get("recovered")
                state_obj.active_now = state.get("active")
                state_obj.delta_confirmed = state.get("deltaconfirmed")
                state_obj.delta_recovered = state.get("deltarecovered")
                state_obj.delta_death = state.get("deltadeaths")
                state_obj.save()
        return response(data="Updated Successfully")
    except Exception as e:
        return response(data=str(e), code=status.HTTP_304_NOT_MODIFIED)


def update_data_state_district_wise():
    response_data = requests.get(UPDATE_STATE_DISTRICT_DATA_URL)
    data = response_data.json()
    for state in data:
        state_obj = State.objects.filter(name=state).first()
        if state_obj:
            district_data = data[state].get("districtData")
            for dist in district_data:
                district = District.objects.filter(state=state_obj.id, name=dist).first()
                if district:
                    dist_data = district_data[dist]
                    district.patients = dist_data.get("confirmed")
                    district.save()
                else:
                    dist_data = district_data[dist]
                    District.objects.create(state=state_obj, name=dist, patients=dist_data.get("confirmed"))
    return data


def get_about_page(request):
    return render(request, template_name="about.html")


def get_safety_template(request):
    return render(request, template_name='safety.html')


def create_country_and_states():
    try:
        country = Country.objects.get(name="India")
        return response(data="for this API first delete the db otherwise object ids will mismatch "
                             "then ~/.manage.py migrate")
    except ObjectDoesNotExist:
        country = Country.objects.create(name="India", population=1354000000)
    finally:
        state = State.objects.all()
        if state:
            return response(data="for this API first delete the db otherwise object ids will mismatch "
                                 "then ~/.manage.py migrate")
        for name, population in INDIAN_STATES.items():
            State.objects.create(country=country, name=name, population=population)
        return response(data="created data successfully")
