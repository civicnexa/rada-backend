from django.db import models

# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=500)
    start_date = models.DateTimeField()