from django.db import models
from django.db.models import Manager


# Create your models here.
class ModelBase(models.Model):
    """
    Model to save created at and updated at time and date
    """
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract=True


class Country(ModelBase):

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
    last_updated = models.DateTimeField()

    objects = Manager()

    def __str__(self):
        return f"{self.name}"

    @property
    def get_state(self):
        return [state for state in self.state_set.all()]


class State(ModelBase):

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

    def __str__(self):
        return f"{self.name} - {self.patients}"

    @property
    def get_district(self):
        return [dist for dist in self.district_set.order_by('patients')]


class District(ModelBase):

    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    patients = models.IntegerField()

    objects = Manager()

    def __str__(self):
        return f"{self.name}"
