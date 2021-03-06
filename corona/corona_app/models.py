from django.db import models
from django.db.models import Manager
from datetime import timedelta


# Create your models here.
class ModelBase(models.Model):
    """
    Model to save created at and updated at time and date
    """
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class Country(ModelBase):
    """
    Model to save country with all patient count i.e death, confirmed etc
    name : country name
    population : population of country
    patients : confirmed patients in country
    help_line_number : central help line no. for corona emergency
    active_now : currently active patient in country
    death : country casualties
    recovered : recovered patient count in country
    delta_confirmed : current day count of confirmed in country
    delta_death : current day count of casualties in country
    delta_recovered : current day count of recovered in country
    last_updated : datetime when data got updated in db
    """
    name = models.CharField(max_length=255, unique=True)
    population = models.CharField(max_length=255)
    recovered = models.IntegerField(default=0)
    death = models.IntegerField(default=0)
    active_now = models.IntegerField(default=0)
    patients = models.IntegerField(default=0)
    help_line_number = models.CharField(max_length=100, blank=True, null=True, default=104)
    delta_confirmed = models.IntegerField(default=0)
    delta_death = models.IntegerField(default=0)
    delta_recovered = models.IntegerField(default=0)

    objects = Manager()

    @property
    def get_last_updated(self):
        """
        return IST
        """
        dt = self.modified_at + timedelta(0, 19800)
        return dt.strftime("%H:%M")

    @property
    def get_state(self):
        """
        property to extract all state in list related to country
        """
        return [state for state in self.state_set.all()]


class State(ModelBase):
    """
    Model to save state with all patient count i.e death, confirmed etc
    country : foreign key of country (country -> state i.e one to many)
    name : state name
    population : population of state
    patients : confirmed patients in state
    help_line_number : state help line no. for corona emergency
    active_now : currently active patient in state
    death : state casualties
    recovered : recovered patient count in state
    delta_confirmed : current day count of confirmed in state
    delta_death : current day count of casualties in state
    delta_recovered : current day count of recovered in state
    """
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    population = models.CharField(max_length=100)
    patients = models.IntegerField(default=0)
    help_line_number = models.CharField(max_length=100, blank=True, null=True, default=104)
    active_now = models.IntegerField(default=0)
    death = models.IntegerField(default=0)
    recovered = models.IntegerField(default=0)
    delta_confirmed = models.IntegerField(default=0)
    delta_death = models.IntegerField(default=0)
    delta_recovered = models.IntegerField(default=0)

    objects = Manager()

    @property
    def get_district(self):
        """
        property to extract all district in list related to state
        """
        return [dist for dist in self.district_set.all()]


class District(ModelBase):
    """
    Model to save district data i.e name & patient
    state : foreign key of state (state -> district i.e one to many)
    name : name of district
    patients : confirmed patients in district
    """
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    patients = models.IntegerField()
    active_now = models.IntegerField(default=0)
    death = models.IntegerField(default=0)
    recovered = models.IntegerField(default=0)
    delta_confirmed = models.IntegerField(default=0)
    delta_death = models.IntegerField(default=0)
    delta_recovered = models.IntegerField(default=0)

    objects = Manager()


class CaseTimeSeries(ModelBase):
    """
    Model to save case time series of corona patients
    date_str : date string
    total_confirmed : total confirmed till date
    total_recovered : total recovered till date
    total_death : total casualties till date
    delta_confirmed : confirmed on current date
    delta_recovered : recovered on current date
    delta_death : casualties on current date
    """
    date_str = models.CharField(max_length=50, unique=True)
    total_confirmed = models.IntegerField()
    total_recovered = models.IntegerField()
    total_death = models.IntegerField()
    delta_confirmed = models.IntegerField()
    delta_recovered = models.IntegerField()
    delta_death = models.IntegerField()

    objects = Manager()
