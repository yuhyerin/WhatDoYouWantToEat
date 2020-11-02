from django.db import models
from django.conf import settings
from stores.models import Store

class Advertisement(models.Model):
    # 광고주 정보
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    # store랑 연결시키면 category 정보도 알 수 있다.
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(null=True, blank=True, upload_to='ad')
    created_at = models.DateTimeField(auto_now_add=True)
   

class AdvertisementClick(models.Model):
    # 클릭한 유저 정보
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.SET_NULL, null=True)
