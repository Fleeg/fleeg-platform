from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from notification.models import Notification


class NotificationView:
    @staticmethod
    @login_required
    def list(request):
        owner = request.user.accounts.first()
        notifications = Notification.objects.filter(owner=owner)
        return render(request, 'home.html', {'notifications': notifications})
