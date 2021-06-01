from django.db import models

class TravelInfo(models.Model):
    to_Location = models.CharField(default="", max_length=50)
    from_Location = models.CharField(default="", max_length=50)
    date = models.CharField(default="", max_length=50)
    busID = models.CharField(default="", max_length=50)
    email = models.EmailField(default="", max_length=254)
