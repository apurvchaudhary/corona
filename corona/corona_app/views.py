from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from corona_app.models import Country, State
from corona_app.serializers import StateSerializer, CountrySerializer
from corona_app.utils import get_graph_data


def response(data, code=status.HTTP_200_OK):
    """
    Overrides rest_framework response
    :param data: data to be send in response
    :param code: response status code(default has been set to 200)
    :param error: error message(if any, not compulsory)
    """
    return Response(data=data, status=code)

# Create your views here.
class CountryView(APIView):

    def get(self, request):
        try:
            country = Country.objects.get(name='india')
        except ObjectDoesNotExist:
            return response(data="No country with this name", code=status.HTTP_404_NOT_FOUND)
        else:
            countryserializer = CountrySerializer(country)
            return render(request, template_name='home.html', context={'data': countryserializer.data})


class SafetyView(APIView):

    def get(self, request):
        return render(request, template_name='safetytips.html')


class GraphView(APIView):

    def get(self, request):
        return get_graph_data()
