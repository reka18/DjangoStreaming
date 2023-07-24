from django.db import models
from django.utils import timezone
import json
from utils import safe_loads
from collections import OrderedDict


# Comments can be made on documents or other comments
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=260)
    # reply to other comment
    ref_comment = models.ForeignKey('conversation_manager.Comment', on_delete=models.CASCADE, null=True, blank=True)
    # comment on document
    ref_document = models.ForeignKey('document_manager.Document', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    visible = models.BooleanField(default=True)
    author = models.ForeignKey('user_manager.StreamUser', on_delete=models.CASCADE)
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)

    def __str__(self):
        return f'<COMMENT: {self.text}>'

    def string(self):
        i = {
            'id': self.id,
            'text': self.text,
            'ref_comment': safe_loads(self.ref_comment),
            'ref_document': safe_loads(self.ref_document, True),
            'created_at': self.created_at,
            'visible': self.visible,
            'author': safe_loads(self.author),
            'up_votes': self.up_votes,
            'down_votes': self.down_votes
        }
        return json.dumps(OrderedDict(i), indent=4, default=str)

    def _up_vote(self):
        self.up_votes += 1
        self.save()

    def _down_vote(self):
        self.down_votes += 1
        self.save()

    def _remove(self):
        self.visible = False
        self.save()


# Messages are sent between users
class Message(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=260)
    created_at = models.DateTimeField(default=timezone.now)
    visible = models.BooleanField(default=True)
    sender = models.ForeignKey('user_manager.StreamUser', on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey('user_manager.StreamUser', on_delete=models.CASCADE, related_name='recipient')

    def __str__(self):
        return f'<MESSAGE: {self.text}>'

    def string(self):
        i = {
            'id': self.id,
            'text': self.text,
            'created_at': self.created_at,
            'visible': self.visible,
            'sender': safe_loads(self.sender),
            'recipient': safe_loads(self.recipient),
        }
        return json.dumps(OrderedDict(i), indent=4, default=str)

    def _up_vote(self):
        self.up_votes += 1
        self.save()

    def _down_vote(self):
        self.down_vote += 1
        self.save()

    def _remove(self):
        self.visible = False
        self.save()
