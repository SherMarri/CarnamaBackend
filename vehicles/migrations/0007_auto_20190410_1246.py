# Generated by Django 2.1.5 on 2019-04-10 07:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0006_auto_20190404_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='model',
            name='make',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='models', to='vehicles.Make'),
        ),
    ]
