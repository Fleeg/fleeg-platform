from django.conf.urls import url
from link.views import LinkView, LinkReactionView


urlpatterns = [
    url(r'^$', LinkView.new, name='link_new'),
    url(r'^react/(?P<post_id>[0-9]+)', LinkReactionView.react, name='link_react'),
    url(r'^unreact/(?P<post_id>[0-9]+)', LinkReactionView.unreact, name='link_unreact'),
]
