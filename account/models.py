from django.db import models


class Account(models.Model):
    user = models.ForeignKey(to='auth.User', related_name='accounts')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

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
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('owner', 'follow',)
