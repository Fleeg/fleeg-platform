
class Search:
    def __init__(self, query, executor):
        self.adv_separator = ':'
        self.results = []
        self.executor = executor
        self.query_value = query
        self.words = query.lower().split(' ')

    def process(self):
        if self.is_advanced():
            self.advanced()
        else:
            print('It is not supported yet.')

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
            print('attr not supported! try; user, title or tag')

    def query_users(self):
        # username or first and last name
        print('run user')
        pass

    def query_links_by_title(self):
        pass

    def query_links_by_tag(self):
        pass