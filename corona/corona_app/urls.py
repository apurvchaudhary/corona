from django.urls import re_path
from corona_app.views import CountryView, SafetyView, HomeGraphView, StateView, StateGraphView, \
    UpdateDataView, AboutView, CreateDataView, SearchView, SearchDistrictByNameView, LineGraphView,\
    AllStateBarGraphView, CaseTimeGraphView

urlpatterns = [
    re_path(r'^home/$', CountryView.as_view(), name="home"),
    re_path(r'^safety/$', SafetyView.as_view(), name="safety-tips"),
    re_path(r'^stategraph/$', StateGraphView.as_view(), name="state-graph"),
    re_path(r'^graph/$', HomeGraphView.as_view(), name="graph"),
    re_path(r'^pie/$', HomeGraphView.as_view(), name="pie"),
    re_path(r'^state/$', StateView.as_view(), name="by-state"),
    re_path(r'^updatedata/$', UpdateDataView.as_view(), name="update-data"),
    re_path(r'^createdata/$', CreateDataView.as_view(), name="create-data"),
    re_path(r'^about/$', AboutView.as_view(), name="about"),
    re_path(r'^search/$', SearchView.as_view(), name="search"),
    re_path(r'^searchdistrictbyname/$', SearchDistrictByNameView.as_view(), name="search-by-district-name"),
    re_path(r'^getlinedata/$', LineGraphView.as_view(), name="line-graph-data"),
    re_path(r'^allstatebargraph/$', AllStateBarGraphView.as_view(), name="all-state-bar-graph"),
    re_path(r'^casetimegraph/$', CaseTimeGraphView.as_view(), name="case-time-graph"),
]
