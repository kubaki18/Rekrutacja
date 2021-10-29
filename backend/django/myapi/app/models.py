from django.db import models

# Create your models here.
class Table(models.Model):
    number = models.IntegerField(primary_key=True)
    minNumberOfSeats = models.IntegerField()
    maxNumberOfSeats = models.IntegerField()

class Reservation(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    numberOfSeats = models.IntegerField()
    dateBegin = models.DateTimeField()
    dateFinish = models.DateTimeField()
