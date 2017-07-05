from django.conf.urls import url
from account.views import AuthView, ProfileView


urlpatterns = [
    url(r'^signup/', AuthView.signup, name='account_signup'),
    url(r'^login/', AuthView.login, name='account_login'),
    url(r'^logout/', AuthView.logout_redirect, name='account_logout'),
    url(r'^follow/(?P<username>\w+)', ProfileView.follow, name='account_follow'),
    url(r'^unfollow/(?P<username>\w+)', ProfileView.unfollow, name='account_unfollow'),
]
