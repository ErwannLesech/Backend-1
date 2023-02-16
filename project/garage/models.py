import datetime
from django.contrib import admin
from django.db import models
from django.utils import timezone

class motorcycle(models.Model):
    name = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    pub_date = models.DateField()

    def __str__(self):
        return self.name
    
    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class detail(models.Model):
    motorcycle = models.ForeignKey(motorcycle, on_delete=models.CASCADE)
    description = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.description