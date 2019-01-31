# Generated by Django 2.1.5 on 2019-01-31 00:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20190131_0539'),
        ('vehicles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='make',
            name='region',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='common.Region'),
            preserve_default=False,
        ),
    ]
