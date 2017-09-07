from django.db import models
from link import utils


class Post(models.Model):
    owner = models.ForeignKey(to='account.Account', related_name='own_posts')
    publisher = models.ForeignKey(to='account.Account', related_name='posts')
    url = models.URLField()
    type = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    summary = models.CharField(null=True, max_length=250)
    text = models.TextField(null=True)
    image_url = models.CharField(null=True, max_length=500)
    tags = models.CharField(null=True, max_length=500)
    publish_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_metadata(self):
        page_info = utils.get_page_info(self.url)
        self.type = page_info['type']
        self.title = page_info['title']
        self.summary = page_info['summary']
        self.text = page_info['text']
        self.image_url = page_info['image']
        self.tags = ','.join(page_info['tags'])
        self.publish_date = page_info['publish_date']

    def get_tags_as_list(self):
        return self.tags.split(',')

    @staticmethod
    def list_with_actions(username, user=None):
        qs_reactions = Reaction.objects.filter(post=models.OuterRef('pk'), owner=user)

        return Post.objects.filter(owner__user__username=username).annotate(
                    is_reacted=models.Exists(queryset=qs_reactions)).order_by('-created_at')

    def __str__(self):
        return self.title


class Comment(models.Model):
    owner = models.ForeignKey(to='account.Account')
    post = models.ForeignKey(to='link.Post', related_name='comments')
    text = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


class Reaction(models.Model):
    owner = models.ForeignKey(to='account.Account')
    post = models.ForeignKey(to='link.Post', related_name='reactions')
    type = models.CharField(max_length=50, default='LIKE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.owner.user.first_name + ' ' + self.owner.user.last_name
