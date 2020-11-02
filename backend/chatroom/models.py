from django.db import models
from django.conf import settings


class makeChatroom(models.Model):
    store_id = models.IntegerField(null=False)
    room_name = models.CharField(max_length=100, null=True)
    usercount = models.IntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, null=True)
