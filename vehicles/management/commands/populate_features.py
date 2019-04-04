from django.core.management.base import BaseCommand
import csv
from vehicles import models


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        m = []
        with open('Features.csv') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                m.append(models.Feature(
                    name=row[1], vehicle_type=models.CAR, code=row[6]))
        models.Feature.objects.bulk_create(m)
        print('{0} features added.'.format(len(m)))


