# Generated by Django 2.1.5 on 2019-03-29 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0010_auto_20190326_1959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='transmission_type',
            field=models.IntegerField(choices=[(1, 'Manual'), (2, 'Automatic'), (3, 'CVT'), (4, 'Semi-automatic')]),
        ),
    ]
