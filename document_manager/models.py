from enum import IntEnum

from django.db import models
from django.utils import timezone
from utils import safe_loads
import json
from collections import OrderedDict


class Status(IntEnum):
    BACKLOG = 1
    OPEN = 2
    TODO = 3
    IN_PROGRESS = 4
    IN_REVIEW = 5
    DONE = 6
    CLOSED = 7

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


# Create your models here.
class Document(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    text = models.CharField(max_length=10000)
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)
    tags = models.ManyToManyField('tag_manager.Tag', blank=True)
    status: Status = models.IntegerField(choices=Status.choices(), default=Status.BACKLOG)
    author = models.ForeignKey('user_manager.StreamUser', on_delete=models.CASCADE, related_name='author')
    assignee = models.ForeignKey('user_manager.StreamUser', on_delete=models.CASCADE, related_name='assignee',
                                 null=True, blank=True)
    last_updated_by = models.ForeignKey('user_manager.StreamUser', on_delete=models.CASCADE,
                                        related_name='last_updated_by', null=True,
                                        blank=True)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return f'<DOC: {self.title}>'

    def string(self):
        i = {
            'id': self.id,
            'title': self.title,
            'created_at': self.created_at,
            'text': self.text,
            'up_votes': self.up_votes,
            'down_votes': self.down_votes,
            'tags': self._show_tags(),
            'status': self.status,
            'author': safe_loads(self.author),
            'assignee': safe_loads(self.assignee),
            'last_updated_by': safe_loads(self.last_updated_by),
            'visible': self.visible
        }
        return json.dumps(OrderedDict(i), indent=4, default=str)

    def _show_tags(self) -> str:
        return str([i.name for i in self.tags.all()])

    def _up_vote(self):
        self.up_votes += 1
        self.save()

    def _down_vote(self):
        self.down_votes += 1
        self.save()

    def _change_text(self, editor, new_text):
        self.text = new_text
        self.last_updated_by = editor
        self.save()

    def _change_title(self, editor, new_title):
        self.title = new_title
        self.last_updated_by = editor
        self.save()

    def _change_status(self, editor, new_status):
        self.status = new_status
        self.last_updated_by = editor
        self.save()

    def _add_tag(self, editor, tag):
        self.tags.add(tag)
        self.last_updated_by = editor
        self.save()

    def _remove(self):
        self.visible = False
        self.save()

    def _change_assignee(self, editor, assignee):
        self.assignee = assignee
        self.last_updated_by = editor
        self.save()
