from rest_framework import status
from rest_framework.views import APIView

from corona_app import utils
from corona_app.permissions import Check_API_KEY_Auth


class CountryView(APIView):
    """
    View to get home page
    """
    def get(self, request):
        """
        param : get request
        return : rendered home.html
        """
        return utils.get_country_data(request)


class SafetyView(APIView):
    """
    View to get safety page
    """
    def get(self, request):
        """
        param : get request
        return : rendered safety.html
        """
        return utils.get_safety_template(request)


class HomeGraphView(APIView):
    """
    View to get graph of all state data json {labels : [], data : []}
    """
    def get(self, request):
        """
        param : none
        return : json of labels and their data
        """
        return utils.get_home_graph_data()


class StateView(APIView):
    """
    View to get state page
    """
    def get(self, request):
        """
        param : get request with state_id in query params
        return : rendered state.html
        """
        return utils.get_state_data_by_name(request)


class StateGraphView(APIView):
    """
    View to get state page graph data of all district json {labels : [], data : []}
    """
    def get(self, request):
        """
        param : get request with state_id in query params
        return : json of labels and their data
        """
        return utils.get_state_graph_data(request)


class UpdateDataView(APIView):
    """
    View to update data in db
    required : authentication
    authentication passed : update data
    authentication failed : return error
    """
    permission_classes = (Check_API_KEY_Auth,)

    def put(self, request):
        """
        param : put request with authentication key provided
        return : success
        """
        try:
            utils.update_data_state_district_wise()
        except Exception as e:
            return utils.response(data=str(e), code=status.HTTP_304_NOT_MODIFIED)
        else:
            return utils.update_data_state_wise()


class CreateDataView(APIView):
    """
    View to create data in db when project is setup i.e country, state with mandatory fields
    required : authentication
    authentication passed : create table with columns
    authentication failed : return error
    """
    permission_classes = (Check_API_KEY_Auth,)

    def post(self, request):
        """
        param : post request with authentication key provided
        return : success
        """
        return utils.create_country_and_states()


class AboutView(APIView):
    """
    View to get about page
    """
    def get(self, request):
        """
        param : get request
        return : rendered about.html
        """
        return utils.get_about_page(request)
