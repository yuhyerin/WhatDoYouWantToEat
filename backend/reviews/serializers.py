from rest_framework import serializers
from .models import Review, Reply
from accounts.serializers import UserProfileSerializer

class WholeReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class StoreReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = '__all__'

class ReviewDetailSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    replyset = ReplySerializer(many=True, source='reply_set')
    class Meta:
        model = Review
        fields = ['id', 'content', 'storeid', 'userid', 'score', 'reg_time', 'created_at', 'user', 'replyset']




class ReviewReplySerializer(serializers.ModelSerializer):
    review = ReviewSerializer()
    class Meta:
        model = Reply
        fields = ['id', 'content', 'created_at', 'review']
