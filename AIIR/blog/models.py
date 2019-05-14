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
    duration = models.CharField(null=True, max_length=5)
    seed = models.CharField(max_length=5)
    iterations = models.CharField(max_length=5)
    quarter = models.CharField(max_length=5)
    progress1 = models.DecimalField(decimal_places=0, max_digits=3)
    progress2 = models.DecimalField(decimal_places=0, max_digits=3)
    progress3 = models.DecimalField(decimal_places=0, max_digits=3)
    plane_data1 = models.DecimalField(decimal_places=2, max_digits=3)
    plane_data2 = models.DecimalField(decimal_places=2, max_digits=3)
    plane_data3 = models.DecimalField(decimal_places=2, max_digits=3)
    plane_data4 = models.DecimalField(decimal_places=2, max_digits=3)
    status = models.CharField(max_length=12)
