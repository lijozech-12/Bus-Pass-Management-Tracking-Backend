# Generated by Django 3.2 on 2021-06-01 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('functions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='travelinfo',
            name='date',
            field=models.CharField(default='', max_length=50),
        ),
    ]