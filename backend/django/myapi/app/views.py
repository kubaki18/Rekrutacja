from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ReservationSerializer, TableSerializer
from .models import Reservation, Table

# Create your views here.

