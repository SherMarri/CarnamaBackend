# Generated by Django 2.1.5 on 2019-04-19 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20190419_1558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temporaryuser',
            name='name',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
