from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ReservationGetSerializer, ReservationPostSerializer, ReservationPutSerializer, ReservationDeleteSerializer, VerificationCodeSerializer, TableSerializer, ParamsSerializer
from .models import Reservation, Table, VerificationCode
import datetime
from django.utils import timezone
from django.db.models import Q
from .mail import send_mail
import random

@api_view(['GET', 'POST'])
def reservations(request):
    # 
    # reservations/ GET
    #
    if request.method == 'GET':
        # TODO: add some sort of authentication so only the restaurant's stuff can access the data
        params = request.query_params
        # here's a default value for queried date (only valid if no parameter is given in request)
        queryDateBegin = datetime.date.today()
        # TODO: clean up this mess and get rid of try..except
        if params is not None and 'date' in params.keys():
            # check if client sent a valid date in valid format
            # TODO: add a case for when user sends a datetime with more data than covered here
            try:
                date = datetime.datetime.strptime(params['date'], '%Y-%m-%d')
            except Exception as e:
                print(e)
                return Response("Incorrect date",status=status.HTTP_400_BAD_REQUEST)
            else:
                queryDateBegin = date.date()
        reservations_list = Reservation.objects.filter(dateBegin__date=queryDateBegin)
        serializer = ReservationGetSerializer(reservations_list, many=True, context={'request': request})
        return Response(serializer.data)

    #
    # reservations/ POST
    #
    elif request.method == 'POST':
        serializer = ReservationPostSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = serializer.validated_data
            print(data['dateBegin'])

            # check if dates are in correct order
            if data['dateBegin'] >= data['dateFinish']:
                return Response("You can't finish the reservation before it even begins!",
                    # TODO: make sure if 406 is the correct code, might need to change to 400
                    status=status.HTTP_406_NOT_ACCEPTABLE)
            if data['dateBegin'] < timezone.now():
                return Response("You can't reserve a table in the past!", status=status.HTTP_406_NOT_ACCEPTABLE)

            # filter out any reservations that starts after or ends before the queried time stamp
            conflicting_reservations = Reservation.objects.exclude(Q(dateBegin__gte=data['dateFinish']) | \
                Q(dateFinish__lte=data['dateBegin'])).filter(table=data['table'])
            if conflicting_reservations:
                print(conflicting_reservations)
                return Response("Can't reserve this table at that time", status=status.HTTP_406_NOT_ACCEPTABLE)

            # check if the number of seats is correct
            correctNumberOfSeats = int(data['numberOfSeats']) >= int(data['table'].minNumberOfSeats) and \
                    int(data['numberOfSeats']) <= int(data['table'].maxNumberOfSeats)
            if not correctNumberOfSeats:
                return Response("Incorrect number of seats", status=status.HTTP_406_NOT_ACCEPTABLE)

            serializer.save()
            try:
                # TODO: Clean this absolutely terrible line of code
                res_id = Reservation.objects.get(table=data['table'], dateBegin=data['dateBegin']).reservationID 
                print(res_id)
                send_mail(serializer.validated_data['email'], 
                        f"Subject: Reservation\n\nThe reservation has been placed successfully. Your reservation ID is {res_id}")
            except Exception as e:
                print(e)
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(status=status.HTTP_201_CREATED)

@api_view(['PUT', 'DELETE'])
def reservation_cancel(request, res_id):
    #
    # reservations/<id> PUT
    #
    if request.method == 'PUT':
        cancelled_reservation = Reservation.objects.get(reservationID=res_id)
        request_date = timezone.now()
        if (cancelled_reservation.dateBegin + datetime.timedelta(hours=2)) < request_date:
            return Response("Too late!", status=status.HTTP_406_NOT_ACCEPTABLE)
        if cancelled_reservation.status == "Requested Cancellation":
            return Response("Already in the cancellation process", status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer = VerificationCodeSerializer(data={'timeOfCreation': timezone.now(), 'value': ''.join([random.choice('1234567890') for _ in range(6)])})
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        # TODO: get this object by ID (for some reason I haven't been able to figure it out yet)
        cancelled_reservation.verificationCode = VerificationCode.objects.get(timeOfCreation=serializer.data['timeOfCreation'], value=serializer.data['value'])
        cancelled_reservation.save()
        send_mail(cancelled_reservation.email, f"Subject: Reservation Cancellation Request\n\nYour verification code: {serializer.data['value']}")
        return Response(status=status.HTTP_200_OK)

    #
    # reservations/<id> DELETE
    #
    elif request.method == 'DELETE':
        cancelled_reservation = Reservation.objects.get(reservationID=res_id)
        verification_code = request.query_params['verificationCode']
        if verification_code != cancelled_reservation.verificationCode.value:
            return Response("Incorrect verification code!", status=status.HTTP_400_BAD_REQUEST)
        cancelled_reservation.verificationCode.delete()
        send_mail(cancelled_reservation.email, f"Subject: Reservation Cancelled\n\nYour reservation (ID: {cancelled_reservation.reservationID}) at the table no.{cancelled_reservation.table.number} was cancelled.")
        cancelled_reservation.delete()
        return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def tables(request):
    if request.method == 'GET':
        params = ParamsSerializer(data=request.query_params)
        if not params.is_valid():
            print(params)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        taken_tables = Reservation.objects.exclude(Q(dateBegin__gte=params.validated_data['dateFinish']) | Q(dateFinish__lte=params.validated_data['dateBegin'])).values_list('table')
        tables_list = Table.objects.exclude(number__in=[x[0] for x in taken_tables])
        tables_list = tables_list.filter(minNumberOfSeats__lte=params.validated_data['numberOfSeats'], maxNumberOfSeats__gte=params.validated_data['numberOfSeats'])
        serializer = TableSerializer(tables_list, many=True)
        return Response(serializer.data)
