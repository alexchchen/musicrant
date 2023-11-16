from django.db import models
from django.db.models import CheckConstraint, Q, F

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=15, primary_key=True)
    fname = models.CharField(max_length=15)
    lname = models.CharField(max_length=15)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=15, null=True)
    password = models.CharField(max_length=15)
    admin_flag = models.BooleanField(default=False)
    client_flag = models.BooleanField(default=True)
    date_joined = models.DateField()
    
    class Meta:
        constraints = [
            CheckConstraint(
                check = Q(age__gt=0) & Q(age__lte=120),
                name = 'check_age'
            ),
        ]