from django.db import models


class User(models.Model):
    name = models.CharField(max_length=55)
    surname = models.CharField(max_length=55)
    email = models.EmailField()
    password = models.TextField(max_length=30)


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
    parameter4 = models.CharField(max_length=5)
    parameter5 = models.CharField(max_length=5)
