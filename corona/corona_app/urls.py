from django.urls import re_path

from corona_app.views import search_view, safety_view, case_time_graph_view, all_state_bar_graph_view, about_view, \
    AllStateLabelDataView, StateView, DistrictLabelDataView, UpdateDataView, CreateDataView, SearchDistrictByNameView, \
    CaseTimeLineGraphDataView, CountryView

urlpatterns = [
    re_path(r'^safety//$', safety_view, name="safety-tips"),
    re_path(r'^about//$', about_view, name="about"),
    re_path(r'^search/$', search_view, name="search"),
    re_path(r'^home/$', CountryView.as_view(), name="home"),
    re_path(r'^stategraph/$', DistrictLabelDataView.as_view(), name="state-graph"),
    re_path(r'^graph/$', AllStateLabelDataView.as_view(), name="graph"),
    re_path(r'^pie/$', AllStateLabelDataView.as_view(), name="pie"),
    re_path(r'^state/$', StateView.as_view(), name="by-state"),
    re_path(r'^updatedata/$', UpdateDataView.as_view(), name="update-data"),
    re_path(r'^createdata/$', CreateDataView.as_view(), name="create-data"),
    re_path(r'^searchdistrictbyname/$', SearchDistrictByNameView.as_view(), name="search-by-district-name"),
    re_path(r'^getlinedata/$', CaseTimeLineGraphDataView.as_view(), name="line-graph-data"),
    re_path(r'^allstatebargraph/$', all_state_bar_graph_view, name="all-state-bar-graph"),
    re_path(r'^casetimegraph/$', case_time_graph_view, name="case-time-graph"),
]
