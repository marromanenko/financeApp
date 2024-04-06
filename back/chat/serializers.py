from rest_framework import serializers
from .models import Message
from financeApp.models import CustomUser


class OnlineUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
