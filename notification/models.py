from enum import Enum

from django.db import models


class NotificationType(Enum):
    ADD = 'ADD'
    REACT = 'LIKE'
    COMMENT = 'COMMENT'
    FOLLOW = 'FOLLOW'


class Notification(models.Model):
    owner = models.ForeignKey(to='account.Account', related_name='notifications')
    sender = models.ForeignKey(to='account.Account', related_name='sent_notifications')
    post = models.ForeignKey(to='link.Post', null=True)
    type = models.CharField(max_length=50)
    viewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def check_as_viewed(owner):
        Notification.objects.filter(owner=owner).update(viewed=True)

    @staticmethod
    def add(owner, sender, type, post=None):
        notify = Notification(owner=owner, sender=sender, type=type.value, post=post)
        notify.save()
