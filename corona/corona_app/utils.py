import requests
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework.response import Response

from corona_app.models import State, Country, District
from rest_framework import status
from corona_app.serializers import StateSerializer, CountrySerializer
from corona_app.constants import UPDATE_COUNTRY_DATA_URL, UPDATE_STATE_DISTRICT_DATA_URL


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
        country = Country.objects.get(name='india')
    except ObjectDoesNotExist:
        return response(data="No country with this name", code=status.HTTP_404_NOT_FOUND)
    else:
        total=0
        country_serializer = CountrySerializer(country)
        for state in country_serializer.data.get("state"):
            total+=state["patients"]
        return render(request, template_name='home.html', context={'data': country_serializer.data, 'total' : total})

def get_safety_template(request):
    return render(request, template_name='safetytips.html')

def get_graph_data():
    labels = []
    data = []
    states = State.objects.all()
    serializer = StateSerializer(states, many=True)
    for state in serializer.data:
        labels.append(state["name"])
        data.append(state["patients"])
    return response(data={'labels' : labels, 'data' : data})

def get_state_data_by_name(request):
    state_id = request.query_params.get("state_id")
    if state_id:
        try:
            state = State.objects.get(id=state_id)
        except ObjectDoesNotExist:
            return response(data="No state with this name", code=status.HTTP_404_NOT_FOUND)
        else:
            state_serializer = StateSerializer(state)
            return render(request, template_name="state.html", context={"data" : state_serializer.data})
    return response(data="No state id given", code=status.HTTP_400_BAD_REQUEST)

def get_state_graph_data(request):
    state_id = request.query_params.get("state_id")
    if state_id:
        try:
            state = State.objects.get(id=state_id)
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
        country = Country.objects.get(id=1)
        if active_now and confirmed and death and recovered:
            country.death, country.recovered, country.patients, country.active_now   = death, recovered,\
                                                                                       confirmed, active_now
            country.save()
        for state in data.get("statewise")[1:]:
            state_obj = State.objects.filter(name=state.get("state")).first()
            if state_obj:
                state_obj.patients = state.get("confirmed")
                state_obj.save()
        return response(data="Updated Successfully")
    except Exception as e:
        return response(data=str(e), code=status.HTTP_304_NOT_MODIFIED)

def update_data_state_district_wise():
    try:
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
    except Exception as e:
        return response(data=str(e), code=status.HTTP_304_NOT_MODIFIED)