from django.core.management.base import BaseCommand
from app.models import Table
import json

class Command(BaseCommand):
    help = 'Migrates the seats from json file to SQLite database'
    def handle(self, *args, **options):
        try:
            with open(r'../seats.json') as json_file:
                data = json.load(json_file)
                for entry in data['tables']:
                    t = Table(number=entry['number'], minNumberOfSeats=entry['minNumberOfSeats'], maxNumberOfSeats=entry['maxNumberOfSeats'])
                    t.save()
        except:
            print("Something went wrong while opening the seats.json file!")
