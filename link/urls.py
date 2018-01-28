from django.conf.urls import url
from link.views import LinkView, LinkReactionView, LinkCommentView


urlpatterns = [
    url(r'^$', LinkView.new, name='link_new'),
    url(r'^(?P<post_id>[0-9]+)/add/$', LinkView.add, name='link_add'),
    url(r'^(?P<post_id>[0-9]+)/react/$', LinkReactionView.react, name='link_react'),
    url(r'^(?P<post_id>[0-9]+)/unreact/$', LinkReactionView.unreact, name='link_unreact'),
    url(r'^(?P<post_id>[0-9]+)/comment/$', LinkCommentView.comment, name='link_comment'),
]
