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
        countryserializer = CountrySerializer(country)
        return render(request, template_name='home.html', context={'data': countryserializer.data})

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
