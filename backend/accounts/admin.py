from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Order
from stores.models import Store
from reviews.models import Review, Reply
from advertisements.models import Advertisement, AdvertisementClick

user = get_user_model()

admin.site.register(user)
admin.site.register(Order)
admin.site.register(Store)
admin.site.register(Review)
admin.site.register(Reply)
admin.site.register(Advertisement)
admin.site.register(AdvertisementClick)