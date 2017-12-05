from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from notification.models import Notification


class NotificationView:
    @staticmethod
    @login_required
    def list(request):
        owner = request.user.accounts.first()
        notifications = Notification.objects.filter(owner=owner)
        # FIXME: clean viewed notification and return notify_count == 0
        notify_count = Notification.objects.filter(owner=owner, viewed=False).count()
        return render(request, 'notification/list.html', {'notifications': notifications, 'notify_count': notify_count})
