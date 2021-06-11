from django.db import models
import django

class TravelInfo(models.Model):
    to_Location = models.CharField(default="", max_length=50)
    from_Location = models.CharField(default="", max_length=50)
    date = models.CharField(default="", max_length=50)
    busID = models.CharField(default="", max_length=50)
    email = models.EmailField(default="", max_length=254)


class LocationData(models.Model):
    busID = models.CharField(default="", max_length=50, primary_key=True)
    xCoordinate = models.CharField(default="", max_length=100)
    yCoordinate = models.CharField(default="", max_length=100)
    date = models.DateTimeField(auto_now=True)

class ComplaintRegister(models.Model):
    complaint = models.TextField()
    busID = models.CharField(default="", max_length=100)
    userID = models.CharField(default="", max_length=100)
    date = models.DateTimeField(auto_now=True)

class TripInfo(models.Model):
    busID = models.CharField(default="", max_length=100)
    conductorID = models.CharField(default="", max_length=100)
    date = models.DateTimeField(auto_now=True)
    from_loc = models.CharField(default="", max_length=100)
    to_loc = models.CharField(default="", max_length=100)

