from rest_framework import  serializers
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
        fields = ('id', 'name', 'population', 'patients', 'district')

    def get_population(self, obj):
        return convert_comma_separated(obj.population)


class CountrySerializer(serializers.ModelSerializer):

    state  = StateSerializer(source='get_state', many=True)
    name = serializers.SerializerMethodField()
    population = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = ('name', 'population', 'patients', 'state', 'recovered', 'death', 'active_now')

    def get_name(self, obj):
        return obj.name.upper()

    def get_population(self, obj):
        return convert_comma_separated(obj.population)
