from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)

class Pepe(models.Model):
    command = models.CharField(null=False, unique=True, max_length=32)
    url = models.CharField(null=False, unique=True, max_length=512)

from django.contrib import admin

admin.site.register(Pepe)
