from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from notification.models import Notification


class NotificationView:
    @staticmethod
    @login_required
    def list(request):
        owner = request.user.accounts.first()
        notifications = Notification.objects.filter(owner=owner).order_by('-created_at')
        Notification.check_as_viewed(owner)
        notify_count = 0
        return render(request, 'notification/list.html', {'notifications': notifications,
                                                          'notify_count': notify_count})
