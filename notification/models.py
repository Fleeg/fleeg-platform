from django.db import models


class Notification(models.Model):
    owner = models.ForeignKey(to='account.Account', related_name='notifications')
    sender = models.ForeignKey(to='account.Account', related_name='sent_notifications')
    post = models.ForeignKey(to='link.Post', null=True)
    type = models.CharField(max_length=50)
    viewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def unread_count(username):
        return Notification.objects.filter(viewed=False,
                                           owner__user__username=username).count()

    # TODO: IMPLEMENT QUERY TO GET NOTIFICATIONS CONTENTS
