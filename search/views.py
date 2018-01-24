from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from notification.models import Notification
from search.search import Search, SearchException


class SearchView:

    @staticmethod
    @login_required
    def list(request):
        query = request.GET.get('q', None)
        search = Search(query)
        try:
            search.process()
        except SearchException:
            pass
        notify_count = Notification.objects.filter(owner__user=request.user, viewed=False).count()
        return render(request, 'search/list.html', {'search': search, 'notify_count': notify_count})

