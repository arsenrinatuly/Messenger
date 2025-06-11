from rest_framework import serializers

# from chats.models import Chat, Message
from users.serializers import UserSerializer


class ChatQuerySerializer(serializers.Serializer):
    id = serializers.IntegerField()


class ChatSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    is_group = serializers.BooleanField()
    title = serializers.CharField(max_length=100)
    users = UserSerializer(many=True)
