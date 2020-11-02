from django.db import models
from django.conf import settings


class Store(models.Model):
    store_id = models.IntegerField()
    store_name = models.CharField(max_length=50, null=True)
    category = models.CharField(max_length=50, null=True)
    bigcategory = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=100, null=True)
    latitude = models.CharField(max_length=50, null=True)
    longitude = models.CharField(max_length=50, null=True)
    average_rating = models.DecimalField(
        max_digits=6, decimal_places=1, null=True)
    # start_time = models.TimeField(blank=True, null=True)
    # end_time = models.TimeField(blank=True, null=True)
    start_time = models.CharField(max_length=20, null=True)
    end_time = models.CharField(max_length=20, null=True)
    min_price = models.IntegerField(null=True)
    mon = models.IntegerField(null=True)
    tue = models.IntegerField(null=True)
    wed = models.IntegerField(null=True)
    thu = models.IntegerField(null=True)
    fri = models.IntegerField(null=True)
    sat = models.IntegerField(null=True)
    sun = models.IntegerField(null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, null=True)
