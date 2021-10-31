from django.contrib import admin
from .models import Table, Reservation, VerificationCode

# Register your models here.
admin.site.register(Table)
admin.site.register(Reservation)
admin.site.register(VerificationCode)
