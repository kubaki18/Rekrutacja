from rest_framework import serializers
from .models import Reservation, Table

class ReservationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Reservation
        fields = ('table', 'numberOfSeats', 'dateBegin', 'dateFinish')

class TableSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Table
        fields = ('number', 'minNumberOfSeats', 'maxNumberOfSeats')
