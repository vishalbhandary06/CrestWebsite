from django.db import models

# Create your models here.

class Service(models.Model):
    img = models.ImageField(upload_to='pics')
    desc = models.CharField(max_length=200)

class Product(models.Model):
    img = models.ImageField(upload_to='pics')
    head = models.CharField(max_length=100)
    desc = models.CharField(max_length=500)

class Career(models.Model):
    img = models.ImageField(upload_to='pics')
    head = models.CharField(max_length=100)
    desc = models.CharField(max_length=500)
