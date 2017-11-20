from django.db import models


class Notification(models.Model):
    owner = models.ForeignKey(to='account.Account', related_name='notifications')
    sender = models.ForeignKey(to='account.Account', related_name='sent_notifications')
    type = models.CharField(max_length=50)
    post = models.ForeignKey(to='link.Post', related_name='adds', null=True)
    viewed = models.BooleanField(auto_now=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # TODO: IMPLEMENT QUERY TO GET NOTIFICATIONS CONTENTS
    # TODO: IMPLEMENT QUERY TO GET UNREAD CONTENTS COUNT
