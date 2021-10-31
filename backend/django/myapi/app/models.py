from django.db import models

# Create your models here.
class Table(models.Model):
    number = models.IntegerField(primary_key=True)
    minNumberOfSeats = models.IntegerField()
    maxNumberOfSeats = models.IntegerField()

class VerificationCode(models.Model):
    codeId = models.IntegerField(primary_key=True)
    timeOfCreation = models.DateTimeField()
    value = models.CharField(max_length=6)

class Reservation(models.Model):
    reservationID = models.IntegerField(primary_key=True)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    numberOfSeats = models.IntegerField()
    dateBegin = models.DateTimeField()
    dateFinish = models.DateTimeField()
    status = models.CharField(max_length=60, default="Confirmed")
    email = models.EmailField(max_length=60)
    fullName = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    verificationCode = models.ForeignKey(VerificationCode, on_delete=models.SET_NULL, null=True)
