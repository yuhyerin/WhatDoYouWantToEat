from rest_framework import serializers
from .models import Store
from django.contrib.auth import get_user_model
# from review.models import Review
# from reviews.serializers import ReviewSerializer


class StoreSerializer(serializers.ModelSerializer):
    # reviews = ReviewSerializer(source='review_set', many=True)
    
    class Meta:
        model = Store
        fields = '__all__'


class StoreDetailSerializer(StoreSerializer):
    # 아직 리뷰 DB 없음
    # reviews = ReviewSerializer(source='review_set', many=True)

    class Meta(StoreSerializer.Meta):
        model = Store
        fields = '__all__'
