# Generated by Django 2.1.5 on 2019-01-31 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0005_auto_20190131_0009'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
