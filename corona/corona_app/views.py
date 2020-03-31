from rest_framework.views import APIView
from corona_app import utils


# Create your views here.
class CountryView(APIView):

    def get(self, request):
        return utils.get_country_data(request)


class SafetyView(APIView):

    def get(self, request):
        return utils.get_safety_template(request)


class GraphView(APIView):

    def get(self, request):
        return utils.get_graph_data()
