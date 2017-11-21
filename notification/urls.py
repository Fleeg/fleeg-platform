from django.conf.urls import url
from notification.views import NotificationView


urlpatterns = [
    url(r'^$', NotificationView.list, name='notifications'),
]
