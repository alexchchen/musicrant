from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=15, primary_key=True)
    fname = models.CharField(max_length=15)
    lname = models.CharField(max_length=15)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=15, null=True)
    password = models.CharField(max_length=15)
    adminFlag = models.BooleanField(null=True)
    clientFlag = models.BooleanField(null=True)