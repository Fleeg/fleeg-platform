from django.conf.urls import url
from search.views import SearchView


urlpatterns = [
    url(r'^$', SearchView.list, name='search'),
]
