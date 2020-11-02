from rest_framework import serializers
from .models import Advertisement, AdvertisementClick
from accounts.serializers import UserDetailSerializer
from stores.serializers import StoreSerializer

class AdvertisementSerializer(serializers.ModelSerializer):
    # user = UserDetailSerializer()
    # store = StoreSerializer()
    class Meta:
        model = Advertisement
        # fields = ['id', 'image', 'user', 'store']
        fields = ['id', 'image']


class AdvertisementInfoSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()
    store = StoreSerializer()
    class Meta:
        model = Advertisement
        fields = ['id', 'image', 'user', 'store']


class AdvertisementMainSerializer(serializers.ModelSerializer):
    store = StoreSerializer()
    class Meta:
        model = Advertisement
        fields = ['id', 'image', 'store']


class AdvertisementClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementClick
        fields = '__all__'


class AdvertisementClickInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementClick
        fields = '__all__'