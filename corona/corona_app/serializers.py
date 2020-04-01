from rest_framework import  serializers
from corona_app.models import Country, State, District


class DistrictSerializer(serializers.ModelSerializer):

    class Meta:
        model = District
        fields = ('name', 'patients')

class StateSerializer(serializers.ModelSerializer):

    district = DistrictSerializer(source='get_district', many=True)

    class Meta:
        model = State
        fields = ('id', 'name', 'population', 'patients', 'district')


class CountrySerializer(serializers.ModelSerializer):

    state  = StateSerializer(source='get_state', many=True)
    name = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = ('name', 'population', 'patients', 'state', 'recovered', 'death', 'active_now')

    def get_name(self, obj):
        return obj.name.upper()
