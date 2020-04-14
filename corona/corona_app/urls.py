from django.urls import re_path
from corona_app.views import CountryView, SafetyView, GraphView, StateView, StateGraphView,\
    UpdateDataView, AboutView, CreateDataView


urlpatterns = [
    re_path(r'^home/$', CountryView.as_view(), name="home"),
    re_path(r'^safety/$', SafetyView.as_view(), name="safety-tips"),
    re_path(r'^stategraph/$', StateGraphView.as_view(), name="state-graph"),
    re_path(r'^graph/$', GraphView.as_view(), name="graph"),
    re_path(r'^pie/$', GraphView.as_view(), name="pie"),
    re_path(r'^state/$', StateView.as_view(), name="by-state"),
    re_path(r'^updatedata/$', UpdateDataView.as_view(), name="update-data"),
    re_path(r'^createdata/$', CreateDataView.as_view(), name="create-data"),
    re_path(r'^about/$', AboutView.as_view(), name="about"),
]