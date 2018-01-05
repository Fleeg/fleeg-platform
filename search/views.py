from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from search.search import Search


class SearchView:

    @staticmethod
    @login_required
    def list(request):
        owner = request.user.accounts.first()
        query = request.GET.get('q', None)
        search = Search(query, owner)
        search.process()
        return render(request, 'search/list.html', {'search': search})

