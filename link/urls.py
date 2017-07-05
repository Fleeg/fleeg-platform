from django.conf.urls import url
from link.views import LinkView


urlpatterns = [
    url(r'^$', LinkView.new, name='link_new'),
]
