from django.db import models
from django.utils import timezone
import json
from utils import safe_loads
from collections import OrderedDict


# Create your models here.
class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    tag_creator = models.ForeignKey('user_manager.StreamUser', on_delete=models.CASCADE, null=False, blank=False)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return f'<TAG: {self.name}>'

    def string(self):
        i = {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at,
            'tag_creator': safe_loads(self.tag_creator),
            'visible': self.visible
        }
        return json.dumps(OrderedDict(i), indent=4, default=str)

    def _remove(self):
        self.visible = False
        self.save()
