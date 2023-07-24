from rest_framework import serializers

from conversation_manager.models import Comment, Message


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'ref_comment', 'ref_document', 'created_at',
                  'visible', 'author', 'up_votes', 'down_votes']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'text', 'created_at', 'visible', 'sender', 'recipient',
                  'up_votes', 'down_votes']