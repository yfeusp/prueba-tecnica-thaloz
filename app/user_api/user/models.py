from django.db import models
from django.contrib.auth.models import User


class ActivityReport(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.CASCADE)
    date = models.DateField(auto_now=True)
