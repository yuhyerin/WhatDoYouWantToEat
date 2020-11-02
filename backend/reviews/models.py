from django.db import models
from django.conf import settings
from stores.models import Store


class Review(models.Model):
    storeid = models.IntegerField()
    userid = models.IntegerField(null=True)
    score = models.DecimalField(max_digits=6, decimal_places=1, null=True)
    content = models.TextField(null=True)
    reg_time = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True)


class Reply(models.Model):
    review = models.ForeignKey(Review, on_delete=models.SET_NULL, null=True)
    content = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
