from datetime import datetime

import requests
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response

from corona_app.constants import UPDATE_COUNTRY_DATA_URL, UPDATE_STATE_DISTRICT_DATA_URL, INDIAN_STATES
from corona_app.models import State, Country, District, CaseTimeSeries
from corona_app.serializers import StateSerializer, CountrySerializer, StateWithoutDistrictSerializer,\
    DistrictWithStateNameSerializer, CaseTimeSeriesSerializer


def response(data, code=status.HTTP_200_OK):
    """
    Overrides rest_framework response
    :param data: data to be send in response
    :param code: response status code(default has been set to 200)
    :param error: error message(if any, not compulsory)
    """
    return Response(data=data, status=code)


def get_search_by_name(name):
    """
    param : get request with name of district in query params
    return : rendered search.html with (serialized district data or error)
    """
    name_char_list = list(name)
    error = f"Sorry, either no patients in '{name}' or district spelled incorrectly"
    district = District.objects.filter(name__iexact=name).select_related("state")
    if district:
        district_serializer = DistrictWithStateNameSerializer(district, many=True)
        return district_serializer.data, None, None
    elif len(name_char_list) >= 3:
        related_district_name = District.objects.filter(name__contains=name).values("name")
        if related_district_name:
            related_district_name = [district["name"] for district in related_district_name]
            related_district_name = ", ".join(related_district_name)
        else:
            related_district_name = None
        return None, error, related_district_name
    return None, error, None


def get_country_data():
    country = Country.objects.prefetch_related("state_set").filter(name='India').first()
    country_serializer = CountrySerializer(country)
    return country_serializer.data


def get_all_state_label_and_data():
    labels = []
    data = []
    states = State.objects.order_by("patients")
    serializer = StateWithoutDistrictSerializer(states, many=True)
    for state in serializer.data:
        labels.append(state["name"])
        data.append(state["patients"])
    return {'labels': labels, 'data': data}


def get_state_data_by_id(state_id):
    state = State.objects.prefetch_related("district_set").filter(id=state_id).first()
    state_serializer = StateSerializer(state)
    return state_serializer.data


def get_line_graph_data():
    """
    utility to get json data for line graph
    param : none
    return : json {labels : [], data : []}
    """
    labels = []
    total_confirmed = []
    total_recovered = []
    total_death = []
    case_time_objects = CaseTimeSeries.objects.all()
    case_time_serializer = CaseTimeSeriesSerializer(case_time_objects, many=True)
    for case in case_time_serializer.data:
        labels.append(case["date_str"])
        total_confirmed.append(case["total_confirmed"])
        total_recovered.append(case["total_recovered"])
        total_death.append(case["total_death"])
    return {"labels": labels, "total_confirmed": total_confirmed, "total_recovered": total_recovered,
            "total_death": total_death}


def update_data_state_wise():
    """
    utility to update fields of country & state via consuming covid19.org APIs
    param : none
    return : success or error
    """
    response_data = requests.get(UPDATE_COUNTRY_DATA_URL)
    data = response_data.json()
    update_case_time_series(cases_time_series=data.get("cases_time_series"))
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
    if "corona_home" in cache:
        cache.delete("corona_home")
    cache.set("corona_home", get_country_data())
    if "all_state_label_data" in cache:
        cache.delete("all_state_label_data")
    cache.set("all_state_label_data", get_all_state_label_and_data())
    return response(data="Updated Successfully")


def update_data_state_district_wise():
    """
    utility to update/create fields of district via consuming covid19.org APIs
    param : none
    return : success or error
    """
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
            key = "stateid:" + str(state_obj.id)
            if key in cache:
                cache.delete(key)
            cache.set(key, get_state_data_by_id(state_obj.id))
    return data


def update_case_time_series(cases_time_series):
    """
    utility to update/create case time series via consuming covid19.org APIs and set cache
    param : response_data
    return : none
    """
    for case in cases_time_series:
        try:
            CaseTimeSeries.objects.get(date_str=case.get("date"))
        except ObjectDoesNotExist:
            CaseTimeSeries.objects.create(date_str=case.get("date"), total_confirmed=case.get("totalconfirmed"),
                                          total_recovered=case.get("totalrecovered"),
                                          total_death=case.get("totaldeceased"),
                                          delta_confirmed=case.get("dailyconfirmed"),
                                          delta_recovered=case.get("dailyrecovered"),
                                          delta_death=case.get("dailydeceased"))
    if "case_time_line_graph_data" in cache:
        cache.delete("case_time_line_graph_data")
    cache.set("case_time_line_graph_data", get_line_graph_data())


def create_country_and_states():
    """
    utility to create country & state in db
    call this func only when db created newly otherwise row ids will mismatch
    or else delete db and migrate again and call this func
    because in template state_id calls are specific to row id in db
    param : none
    return : success or error
    """
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
