from django.db import models
from django.db.models import Manager
from datetime import datetime

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

    objects = Manager()

    def __str__(self):
        return f"{self.name} - {self.patients}"


class History(ModelBase):

    date = models.DateTimeField()
    state = models.ForeignKey(State, on_delete=models.CASCADE, default=0)
    previous = models.IntegerField()
    now = models.IntegerField()

    objects = Manager()

    def __str__(self):
        return f"{self.date} - {self.now}"
