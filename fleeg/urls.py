from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from account.views import AuthView, ProfileView
from link.views import LinkView


urlpatterns = [
    url(r'^$', AuthView.home_redirect, name='index'),
    url(r'^home/', LinkView.wall, name='home'),
    url(r'^account/', include('account.urls')),
    url(r'^link/', include('link.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^(?P<username>\w+)/$', ProfileView.posts, name='profile'),
    url(r'^(?P<username>\w+)/following', ProfileView.following, name='following'),
    url(r'^(?P<username>\w+)/followers', ProfileView.followers, name='followers'),
    url(r'^(?P<username>\w+)/links', LinkView.links, name='links'),
]
