from django.db import models


class User(models.Model):
    email = models.CharField(max_length=30)
    firs_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
