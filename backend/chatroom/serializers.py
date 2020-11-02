from rest_framework import serializers
from .models import makeChatroom

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = makeChatroom
        fields = '__all__'