# Generated by Django 3.2 on 2021-06-06 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('functions', '0003_locationdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComplaintRegister',
            fields=[
                ('complaintID', models.CharField(auto_created=True, max_length=50, primary_key=True, serialize=False)),
                ('complaint', models.TextField()),
                ('busID', models.CharField(default='', max_length=100)),
            ],
        ),
    ]