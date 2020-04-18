from rest_framework import status
from rest_framework.views import APIView
from corona_app import utils
from corona_app.permissions import Check_API_KEY_Auth


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


class StateView(APIView):

    def get(self, request):
        return utils.get_state_data_by_name(request)


class StateGraphView(APIView):

    def get(self, request):
        return utils.get_state_graph_data(request)


class UpdateDataView(APIView):
    permission_classes = (Check_API_KEY_Auth,)

    def put(self, request):
        try:
            utils.update_data_state_district_wise()
        except Exception as e:
            return utils.response(data=str(e), code=status.HTTP_304_NOT_MODIFIED)
        else:
            return utils.update_data_state_wise()


class CreateDataView(APIView):
    permission_classes = (Check_API_KEY_Auth,)

    def post(self, request):
        return utils.create_country_and_states()


class AboutView(APIView):

    def get(self, request):
        return utils.get_about_page(request)
