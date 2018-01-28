from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from notification.models import Notification
from account.models import Account
from search.search import Search, SearchException


class SearchView:

    @staticmethod
    @login_required
    def list(request):
        query = request.GET.get('q', None)
        anonymous = request.GET.get('anonymous', False)
        owner = None

        if not anonymous:
            owner = Account.get_by_user(request.user)

        try:
            search = Search(query, owner)
            search.process()
        except SearchException:
            pass

        notify_count = Notification.objects.filter(owner__user=request.user, viewed=False).count()
        return render(request, 'search/list.html', {'search': search, 'notify_count': notify_count})
