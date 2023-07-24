from rest_framework import serializers

from user_manager.models import StreamUser


class StreamUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreamUser
        fields = ['username', 'email', 'password', 'is_staff', 'is_superuser']
