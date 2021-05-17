from django.db import models


class UserInfo(models.Model):
    firstName = models.CharField(default="", max_length=50)
    lastName = models.CharField(default="", max_length=50)
    isStudent = models.BooleanField(default=False)
    accBalance = models.FloatField(default=0.0)
    phoneNo = models.CharField(default="", max_length=50)
    email = models.EmailField(default="", max_length=254, primary_key=True)

    class Meta:
        app_label = 'userRegistration'

class UserImage(models.Model):
    userID = models.CharField(default="", max_length=50, primary_key=True)
    pic = models.CharField(default="", max_length=1000)

class ConductorInfo(models.Model):
    firstName = models.CharField(default="", max_length=50)
    lastName = models.CharField(default="", max_length=50)
    phoneNo = models.CharField(default="", max_length=50)
    email = models.EmailField(default="", max_length=254, primary_key=True)
    verified = models.BooleanField(default=False)

    class Meta:
        app_label = 'userRegistration'


class BusPass(models.Model):
    userID = models.CharField(default="", max_length=50, primary_key=True)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    passCode = models.CharField(default="", max_length=50)

    class Meta:
        app_label = 'userRegistration'
