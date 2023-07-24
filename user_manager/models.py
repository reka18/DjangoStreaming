from datetime import datetime

from actstream import action
from conversation_manager.models import Comment, Message
from django.db import models
from document_manager.models import Document
from tag_manager.models import Tag
from django.contrib.auth.models import User
from actstream.models import user_stream
import json
from collections import OrderedDict


# Create your models here.
# noinspection PyProtectedMember
class StreamUser(User):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_stream(self, with_user_activity=True)

    def string(self):
        i = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
        }
        return json.dumps(OrderedDict(i), indent=4, default=str)

    class Meta:
        proxy = True

    def create_document(self, title, text, tags: []):
        document = Document(title=title,
                            created_at=datetime.now(),
                            text=text,
                            author=self)
        document.save()
        action.send(self, verb='created', target=document)
        for tag in tags:
            self.add_tag(document, tag)

    def up_vote(self, target):
        target._up_vote()
        target.save()
        action.send(self, verb='up voted', target=target)

    def down_vote(self, target):
        target._down_vote()
        target.save()
        action.send(self, verb='down voted', target=target)

    # Comment on document
    def comment(self, document, comment):
        comment = Comment(text=comment,
                          author=self,
                          ref_document=document,
                          created_at=datetime.now())
        comment.save()
        action.send(self, verb='commented', target=document, action_object=comment)

    # Reply to comment
    def reply(self, comment, reply):
        comment = Comment(text=reply,
                          author=self,
                          ref_comment=comment,
                          created_at=datetime.now())
        comment.save()
        action.send(self, verb='replied', target=comment, action_object=comment)

    # Change a document
    def change_text(self, document, new_text):
        document._change_text(self, new_text)
        document.save()
        action.send(self, verb='changed text to', target=document)

    def change_title(self, document, new_title):
        document._change_title(self, new_title)
        document.save()
        action.send(self, verb='changed title to', target=document)

    def change_status(self, document, new_status):
        document._change_status(self, new_status)
        document.save()
        action.send(self, verb='changed status to', target=document)

    def change_assignee(self, document, new_assignee):
        document._change_assignee(self, new_assignee)
        document.save()
        action.send(self, verb='changed assignee to', target=document)

    def add_tag(self, document, text):
        try:
            t = Tag.objects.get(name=text)
        except Tag.DoesNotExist:
            t = self.create_tag(text)
        document._add_tag(self, t)
        document.save()
        action.send(self, verb='added tag to', target=document)

    def create_tag(self, text) -> Tag:
        t = Tag(name=text, created_at=datetime.utcnow(), tag_creator=self)
        t.save()
        action.send(self, verb='created tag', target=t)
        return t

    def message(self, recipient, message):
        m = Message(text=message, sender=self, recipient=recipient)
        m.save()
        action.send(self, verb='messaged', target=recipient, action_object=m)
        return m
