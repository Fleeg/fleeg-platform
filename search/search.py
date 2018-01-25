from django.db.models import Q

from account.models import Account
from link.models import Post


class Search:
    def __init__(self, query, owner=None):
        self.owner = owner
        self.adv_separator = ':'
        self.results = []
        self.query_value = query
        self.words = query.lower().split(' ')

    def process(self):
        if self.is_advanced():
            self.advanced()
        else:
            self.query_level(self.filter_links(), self.filter_users())

    def is_advanced(self):
        return self.adv_separator in self.words[0]

    def advanced(self):
        attr, word = self.words.pop(0).split(self.adv_separator)
        if word:
            self.words = [word] + self.words

        if attr == 'user':
            self.query_level(q_filter_user=self.filter_users())
        elif attr == 'title':
            self.query_level(q_filter_link=self.filter_links_by_title())
        elif attr == 'tag':
            self.query_level(q_filter_link=self.filter_links_by_tag())
        else:
            raise SearchException('Attr not supported! try: user, title or tag')

    def filter_users(self):
        return Q(Q(user__username__in=self.words) |
                 Q(user__first_name__in=self.words) |
                 Q(user__last_name__in=self.words))

    def filter_links(self):
        q_filters = Q()
        for word in self.words:
            q_filters.add(Q(title__icontains=word), Q.OR)
            q_filters.add(Q(url__icontains=word), Q.OR)
            q_filters.add(Q(summary__icontains=word), Q.OR)
            q_filters.add(Q(text__icontains=word), Q.OR)
            q_filters.add(Q(tags__icontains=word), Q.OR)
        return q_filters

    def filter_links_by_title(self):
        q_filters = Q()
        for word in self.words:
            q_filters.add(Q(title__icontains=word), Q.OR)
        return q_filters

    def filter_links_by_tag(self):
        q_filters = Q()
        for word in self.words:
            q_filters.add(Q(tags__icontains=word), Q.OR)
        return q_filters

    def query_level(self, q_filter_link=None, q_filter_user=None):
        levels = [
            {'link': Q(owner=self.owner), 'user': Q(id=self.owner.id)},
            {'link': Q(owner__followers__owner=self.owner), 'user': Q(followers__owner=self.owner)},
            {'link': Q(owner_followers__owner__followers__owner=self.owner),
             'user': Q(followers__owner__followers__owner=self.owner)},
        ]
        last_level = {'link': ~Q(levels[0]['link'] | levels[1]['link'] | levels[2]['link']),
                      'user': ~Q(levels[0]['user'] | levels[1]['user'] | levels[2]['user'])}
        if self.owner:
            for level in levels:
                self.results += self.process_query(q_filter_link, q_filter_user, level)
            self.results += self.process_query(q_filter_link, q_filter_user, last_level)
        else:
            self.results = self.process_query(q_filter_link, q_filter_user)

    @staticmethod
    def process_query(q_filter_link=None, q_filter_user=None, level=None):
        level_results = []

        if level is None:
            level = {'link': Q(), 'user': Q()}

        if q_filter_link:
            q_filter_link.add(level['link'])
            level_results += Post.objects.filter(q_filter_link).annotate(
                result_type='post').order_by('-created_at')
        if q_filter_user:
            q_filter_user.add(level['user'])
            level_results += Account.objects.filter(q_filter_user).annotate(
                result_type='user').order_by('-created_at')

        if q_filter_link and q_filter_user:
            level_results = sorted(level_results, key=lambda item: item['created_at'], reverse=True)
        return level_results


class SearchException(Exception):
    pass
