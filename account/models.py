from django.db import models
from django.core.files.storage import FileSystemStorage


class Account(models.Model):
    user = models.ForeignKey(to='auth.User', related_name='accounts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def user_avatar(self):
        fs = FileSystemStorage()
        if fs.exists(self.user.username + '.jpg'):
            return '/static/avatar/' + self.user.username + '.jpg'
        else:
            return '/static/img/profile/default.jpg'

    def is_following(self, follow):
        return self.following.filter(follow=follow).exists()

    def unfollow(self, follow):
        relationship = self.following.filter(follow=follow).first()
        relationship.delete()

    @staticmethod
    def get_by_user(user):
        return Account.objects.filter(user=user).first()

    @staticmethod
    def get_by_username(username):
        return Account.objects.filter(user__username=username).first()


class Relationship(models.Model):
    owner = models.ForeignKey(to='account.Account', related_name='following')
    follow = models.ForeignKey(to='account.Account', related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('owner', 'follow',)
