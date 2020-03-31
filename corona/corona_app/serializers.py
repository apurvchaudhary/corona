from rest_framework import  serializers
from corona_app.models import Country, State


class StateSerializer(serializers.ModelSerializer):

    class Meta:
        model = State
        fields = ('id', 'name', 'population', 'patients', 'recovered', 'death')


class CountrySerializer(serializers.ModelSerializer):

    state  = StateSerializer(source='get_state', many=True)
    name = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = ('name', 'population', 'state')

    def get_name(self, obj):
        return obj.name.upper()
