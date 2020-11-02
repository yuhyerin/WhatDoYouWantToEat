from django.db import models

# Create your models here.
class Delivery(models.Model):
    store_id = models.IntegerField(null=True)
    store_name = models.CharField(max_length=50, null=True)
    category = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=100, null=True)
    latitude = models.CharField(max_length=50, null=True)
    longitude = models.CharField(max_length=50, null=True)
    userid = models.EmailField(null=True)
    score = models.DecimalField(max_digits=6, decimal_places=1, null=True)
    reg_time = models.DateTimeField()
    day_type = models.CharField(max_length=20)