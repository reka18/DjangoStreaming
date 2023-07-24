from rest_framework import serializers

from tag_manager.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'created_at', 'tag_creator', 'visible']
