# Generated by Django 2.1.5 on 2019-05-08 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0015_auto_20190401_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='modification_type',
            field=models.IntegerField(choices=[(1, '1.8 L'), (2, '2.0 L'), (3, '2.5 L'), (4, '3.5 L'), (5, '5.5 L')]),
        ),
    ]