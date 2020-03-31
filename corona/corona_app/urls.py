from django.urls import re_path
from corona_app.views import CountryView, SafetyView, GraphView


urlpatterns = [
    re_path(r'home/', CountryView.as_view(), name="home"),
    re_path(r'safety/', SafetyView.as_view(), name="safety-tips"),
    re_path(r'graph/', GraphView.as_view(), name="graph"),
    re_path(r'pie/', GraphView.as_view(), name="pie"),
]