from rest_framework.response import Response

from corona_app.models import State, Country
from rest_framework import status
from corona_app.serializers import StateSerializer


def response(data, code=status.HTTP_200_OK):
    """
    Overrides rest_framework response
    :param data: data to be send in response
    :param code: response status code(default has been set to 200)
    :param error: error message(if any, not compulsory)
    """
    return Response(data=data, status=code)

def get_graph_data():
    labels = []
    data = []
    states = State.objects.all()
    serializer = StateSerializer(states, many=True)
    for state in serializer.data:
        labels.append(state["name"])
        data.append(state["patients"])
    return response(data={'labels' : labels, 'data' : data})
