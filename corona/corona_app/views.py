from django.core.cache import cache
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from corona_app import utils
from corona_app.constants import CACHE_TTL
from corona_app.permissions import Check_API_KEY_Auth
from corona.settings import GLOBAL_HOME_URL


def response(data, code=status.HTTP_200_OK):
    """
    Overrides rest_framework response
    :param data: data to be send in response
    :param code: response status code(default has been set to 200)
    :param error: error message(if any, not compulsory)
    """
    return Response(data=data, status=code)


@api_view()
@cache_page(CACHE_TTL)
def safety_view(request):
    """
    View to get safety page
    """
    return render(request, template_name="safety.html")


@api_view()
@cache_page(CACHE_TTL)
def about_view(request):
    """
    View to get about page
    """
    return render(request, template_name="about.html", context={"global_home" : GLOBAL_HOME_URL})


@api_view()
@cache_page(CACHE_TTL)
def search_view(request):
    """
    View to get search page
    """
    return render(request, template_name="search.html")


@api_view()
@cache_page(CACHE_TTL)
def all_state_bar_graph_view(request):
    """
    View to get all state bar graph page
    """
    return render(request, template_name="allstate.html")


@api_view()
@cache_page(CACHE_TTL)
def case_time_graph_view(request):
    return render(request, template_name="casetime.html")


class CountryView(APIView):
    """
    View to get home page
    """

    def get(self, request):
        """
        param : get request
        return : rendered home.html
        """
        if "corona_home" in cache:
            return render(request, template_name="home.html", context={"data": cache.get("corona_home")})
        data = utils.get_country_data()
        cache.set("corona_home", data)
        return render(request, template_name="home.html", context={"data": data})


class AllStateLabelDataView(APIView):
    """
    View to get graph of all state data json {labels : [], data : []}
    """

    def get(self, request):
        """
        param : request
        return : json of labels and their data
        """
        if "all_state_label_data" in cache:
            return utils.response(data=cache.get("all_state_label_data"))
        data = utils.get_all_state_label_and_data()
        cache.set("all_state_label_data", data)
        return response(data=data)


class StateView(APIView):
    """
    View to get state page
    """

    def get(self, request):
        """
        param : get request with state_id in query params
        return : rendered state.html
        """
        state_id = request.query_params.get("state_id")
        if state_id:
            if "stateid:" + state_id in cache:
                return render(request, template_name="state.html", context={"data": cache.get("stateid:" + state_id)})
            data = utils.get_state_data_by_id(state_id)
            cache.set("stateid:" + state_id, data)
            return render(request, template_name="state.html", context={"data": data})
        return response(data="No state_id in params", code=status.HTTP_404_NOT_FOUND)


class DistrictLabelDataView(APIView):
    """
    View to get state page graph data of all district json {labels : [], data : []}
    """

    def get(self, request):
        """
        param : get request with state_id in query params
        return : json of labels and their data
        """
        state_id = request.query_params.get("state_id")
        big_state = request.query_params.get("big_state")
        if state_id:
            labels = []
            values = []
            if "stateid:" + state_id in cache:
                data = cache.get("stateid:" + state_id)
                if big_state:
                    for district in data["district"][38:]:
                        labels.append(district["name"])
                        values.append(district["active_now"])
                    return response(data={"labels": labels, "data": values})
                for district in data["district"][:38]:
                    labels.append(district["name"])
                    values.append(district["active_now"])
                return response(data={"labels": labels, "data": values})
            response(data="No state_id in cache", code=status.HTTP_404_NOT_FOUND)
        response(data="No state_id provided", code=status.HTTP_400_BAD_REQUEST)


class SearchDistrictByNameView(APIView):
    """
    View to get Searched District name
    """

    def get(self, request):
        """
        param : get request with district name in query param
        return : rendered search.html with district serialized data
        """
        name = request.query_params.get("name")
        if name:
            data, error, related_name = utils.get_search_by_name(name)
            return render(request, template_name="search.html",
                          context={"data": data, "error": error, "related_name": related_name})
        return render(request, template_name="search.html",
                          context={"data": None, "error": "Sorry, empty district name provided", "related_name": None})


class CaseTimeLineGraphDataView(APIView):
    """
    View to get line graph labels & data
    """

    def get(self, request):
        """
        param : get request
        return : rendered label & data json
        """
        if "case_time_line_graph_data" in cache:
            return response(data=cache.get("case_time_line_graph_data"))
        data = utils.get_line_graph_data()
        cache.set("case_time_line_graph_data", data)
        return response(data=data)


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
