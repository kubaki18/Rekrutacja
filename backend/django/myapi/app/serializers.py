from rest_framework import serializers
from .models import Reservation, Table, VerificationCode

class ReservationGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('reservationID', 'table', 'numberOfSeats', 'dateBegin', 'dateFinish', 'status')

class ReservationPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('table', 'numberOfSeats', 'dateBegin', 'dateFinish', 'email')

class ReservationPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('reservationID', 'dateBegin',
                'status', 'email')

class ReservationDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['reservationID', 'verificationCode']

class VerificationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationCode
        fields = ['timeOfCreation', 'value']

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ('number', 'minNumberOfSeats', 'maxNumberOfSeats')

class ParamsSerializer(serializers.Serializer):
    dateBegin = serializers.DateTimeField()
    dateFinish = serializers.DateTimeField()
    numberOfSeats = serializers.IntegerField()
