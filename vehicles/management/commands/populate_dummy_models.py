from django.core.management.base import  BaseCommand, CommandError
import csv
from vehicles import models


class Command(BaseCommand):
    help = 'Display current time'

    def handle(self, *args, **kwargs):
        m = []
        with open('DummyModels.csv') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                m.append(models.Model(name=row[1], make_id=3))
        models.Model.objects.bulk_create(m)
        print('{0} models added.'.format(len(m)))


