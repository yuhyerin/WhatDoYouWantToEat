from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Order

User = get_user_model()

# MyUser 모델은 User 객체의 OneToOneField 로 생성했다.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        # extra_kwargs = {
        #                 "password": {"write_only": True},
        #                 }


class UserDetailSerializer(UserSerializer):
    class Meta:
        model = User
        # fields = ['id', 'username', 'email', 'usertype', 'gender', 'address', 'date_of_birth', 'biznumber', 'bizname', 'bizimage', 'bizaddress']
        fields = ['id', 'username', 'email', 'usertype', 'gender', 'address', 'birth_year', 'biznumber', 'bizname', 'bizcategory', 'bizimage', 'bizaddress']


class UserProfileSerializer(UserDetailSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'usertype', 'gender', 'address', 'birth_year']


class UserProfileUpdateSerializer(UserDetailSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'usertype', 'gender', 'address', 'birth_year']


class BizUserProfileSerializer(UserDetailSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserOrderListSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'location', 'created_at']
        # fields = ['location']


class UserOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'location', 'created_at']