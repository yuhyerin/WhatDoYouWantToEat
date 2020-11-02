from django.db import models
from django.conf import settings

class RecommendFood(models.Model):
    food = models.CharField(max_length=100, null=True)
