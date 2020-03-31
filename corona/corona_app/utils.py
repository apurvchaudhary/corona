from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework.response import Response

from corona_app.models import State, Country
from rest_framework import status
from corona_app.serializers import StateSerializer, CountrySerializer


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
        recovered=0
        death=0
        country_serializer = CountrySerializer(country)
        for state in country_serializer.data.get("state"):
            total+=state["patients"]
            recovered+=state["recovered"]
            death+=state["death"]
        return render(request, template_name='home.html', context={'data': country_serializer.data, 'total' : total,
                                                                   'recovered' : recovered, 'death' : death})

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
            labels = ["Patients", "Recovered", "Death"]
            data = []
            data.append(state.patients)
            data.append(state.recovered)
            data.append(state.death)
            return response(data={'labels': labels, 'data': data})
    return response(data="No state id given", code=status.HTTP_400_BAD_REQUEST)