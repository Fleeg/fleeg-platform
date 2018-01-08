from django.db.models import Q

from account.models import Account
from link.models import Post


class Search:
    def __init__(self, query):
        self.adv_separator = ':'
        self.results = []
        self.query_value = query
        self.words = query.lower().split(' ')

    def process(self):
        if self.is_advanced():
            self.advanced()
        else:
            self.query_links()
            self.query_users()

    def is_advanced(self):
        return self.adv_separator in self.words[0]

    def advanced(self):
        attr, word = self.words.pop(0).split(self.adv_separator)
        if word:
            self.words = [word] + self.words

        if attr == 'user':
            self.query_users()
        elif attr == 'title':
            self.query_links_by_title()
        elif attr == 'tag':
            self.query_links_by_title()
        else:
            # TODO: Throws a exception
            print('attr not supported! try: user, title or tag')

    def query_users(self):
        accounts = Account.objects.filter(Q(user__username__in=self.words) |
                                          Q(user__first_name__in=self.words) |
                                          Q(user__last_name__in=self.words))
        self.results += list(map(lambda i: self.result_type(i, 'user'), accounts))

    def query_links_by_title(self):
        q_filters = Q()
        for word in self.words:
            q_filters.add(Q(title__icontains=word), Q.OR)

        posts = Post.objects.filter(q_filters)
        self.results = list(map(lambda i: self.result_type(i, 'post'), posts))

    def query_links_by_tag(self):
        q_filters = Q()
        for word in self.words:
            q_filters.add(Q(tags__icontains=word), Q.OR)

        posts = Post.objects.filter(q_filters)
        self.results = list(map(lambda i: self.result_type(i, 'post'), posts))

    def query_links(self):
        q_filters = Q()
        for word in self.words:
            q_filters.add(Q(title__icontains=word), Q.OR)
            q_filters.add(Q(url__icontains=word), Q.OR)
            q_filters.add(Q(summary__icontains=word), Q.OR)
            q_filters.add(Q(text__icontains=word), Q.OR)
            q_filters.add(Q(tags__icontains=word), Q.OR)

        # TODO: Add a for to add rank value based level search
        posts = Post.objects.filter(q_filters)
        self.results += list(map(lambda i: self.result_type(i, 'post'), posts))

    @staticmethod
    def result_type(item, r_type):
        item.result_type = r_type
        return item
