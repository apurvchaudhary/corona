from rest_framework import  serializers
from datetime import timedelta
from corona_app.models import Country, State, District
from corona_app.services import convert_comma_separated


class DistrictSerializer(serializers.ModelSerializer):

    class Meta:
        model = District
        fields = ('name', 'patients')

class StateSerializer(serializers.ModelSerializer):

    district = DistrictSerializer(source='get_district', many=True)
    population = serializers.SerializerMethodField()

    class Meta:
        model = State
        fields = ('id', 'name', 'population', 'patients', 'district', 'active_now', 'death',
                  'recovered', 'help_line_number', 'delta_confirmed', 'delta_recovered', 'delta_death')

    def get_population(self, obj):
        return convert_comma_separated(obj.population)


class StateWithoutDistrictSerializer(serializers.ModelSerializer):

    population = serializers.SerializerMethodField()

    class Meta:
        model = State
        fields = ('id', 'name', 'population', 'patients', 'active_now', 'death',
                  'recovered', 'help_line_number', 'delta_confirmed', 'delta_recovered', 'delta_death')

    def get_population(self, obj):
        return convert_comma_separated(obj.population)


class CountrySerializer(serializers.ModelSerializer):

    state  = StateWithoutDistrictSerializer(source='get_state', many=True)
    name = serializers.SerializerMethodField()
    population = serializers.SerializerMethodField()
    last_updated = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = ('name', 'population', 'patients', 'state', 'recovered', 'death', 'active_now',
                  'help_line_number', 'delta_confirmed', 'delta_recovered', 'delta_death', 'last_updated')

    def get_name(self, obj):
        return obj.name.upper()

    def get_population(self, obj):
        return convert_comma_separated(obj.population)

    def get_last_updated(self, obj):
        dt = obj.last_updated + timedelta(0,19800)
        return dt.strftime("%H:%M")
