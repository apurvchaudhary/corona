from django.contrib import admin
from corona_app.models import Country, State, District

# Register your models here.
admin.site.register([Country, State, District])
