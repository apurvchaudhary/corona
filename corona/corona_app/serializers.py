from rest_framework import serializers
from datetime import timedelta

from corona_app.models import Country, State, District
from corona_app.services import convert_comma_separated


class DistrictSerializer(serializers.ModelSerializer):
    """
    Serializer to serialize district fields i.e name & patients
    """

    class Meta:
        model = District
        fields = ('name', 'patients')


class StateSerializer(serializers.ModelSerializer):
    """
    Serializer to serialize state fields i.e
    id : state id auto created as primary key in db by django
    fields : __all__ state model fields except created_at & updated_at
    district : list of all district serialized data
    """
    district = DistrictSerializer(source='get_district', many=True)
    population = serializers.SerializerMethodField()

    class Meta:
        model = State
        fields = ('id', 'name', 'population', 'patients', 'active_now', 'death',
                  'recovered', 'help_line_number', 'delta_confirmed', 'delta_recovered',
                  'delta_death', 'district')

    def get_population(self, obj):
        """
        population integer converted to comma separated str
        eg: 120000 to 1,20,000
        """
        return convert_comma_separated(obj.population)


class StateWithoutDistrictSerializer(serializers.ModelSerializer):
    """
    Serializer to serialize state fields i.e
    id : state id auto created as primary key in db by django
    fields : __all__ state model fields except created_at & updated_at
    diff bw StateSerializer & StateWithoutDistrictSerializer is
    StateWithoutDistrictSerializer does not have district field in which district
    querying is obsolete
    """
    population = serializers.SerializerMethodField()

    class Meta:
        model = State
        fields = ('id', 'name', 'population', 'patients', 'active_now', 'death',
                  'recovered', 'help_line_number', 'delta_confirmed', 'delta_recovered', 'delta_death')

    def get_population(self, obj):
        """
        population integer converted to comma separated str
        eg: 120000 to 1,20,000
        """
        return convert_comma_separated(obj.population)


class CountrySerializer(serializers.ModelSerializer):
    """
    Serializer to serialize country fields i.e
    id : state id auto created as primary key in db by django
    fields : __all__ country model fields except created_at & updated_at
    state : list of all state serialized data
    """
    state = StateWithoutDistrictSerializer(source='get_state', many=True)
    name = serializers.SerializerMethodField()
    population = serializers.SerializerMethodField()
    last_updated = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = ('name', 'population', 'patients', 'recovered', 'death', 'active_now',
                  'help_line_number', 'delta_confirmed', 'delta_recovered', 'delta_death',
                  'last_updated', 'state')

    def get_name(self, obj):
        """
        method to convert str into upper case
        """
        return obj.name.upper()

    def get_population(self, obj):
        """
        population integer converted to comma separated str
        eg: 120000 to 1,20,000
        """
        return convert_comma_separated(obj.population)

    def get_last_updated(self, obj):
        """
        converted UTC to IST
        """
        dt = obj.last_updated + timedelta(0, 19800)
        return dt.strftime("%H:%M")
