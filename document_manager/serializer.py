from rest_framework import serializers

from document_manager.models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'created_at', 'text', 'up_votes', 'down_votes', 'tags',
                  'status', 'author', 'assignee', 'last_updated_by', 'visible']