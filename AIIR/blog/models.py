from django.db import models
from django.contrib.auth.models import User


class Algorithm(models.Model):
    algorithm_name = models.CharField(max_length=255)
    algorithm_description = models.CharField(max_length=500)


class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    algorithm = models.ForeignKey(Algorithm, on_delete=models.CASCADE)
    image_url = models.URLField()
    date = models.DateTimeField()
    parameter1 = models.CharField(max_length=5)
    parameter2 = models.CharField(max_length=5)
    parameter3 = models.CharField(max_length=5)
    progress1 = models.CharField(max_length=5)
    progress2 = models.CharField(max_length=5)
    progress3 = models.CharField(max_length=5)
    status = models.CharField(max_length=12)
