import factory

from account.factories import AccountFactory
from link.models import Post, Comment, Reaction


class PostFactory(factory.DjangoModelFactory):
    class Meta:
        model = Post

    owner = factory.SubFactory(AccountFactory)
    publisher = factory.SubFactory(AccountFactory)
    url = 'http://test.tst'
    type = 'html'
    title = factory.sequence(lambda n: 'Title Link Test {}'.format(n))
    summary = factory.sequence(lambda n: 'Summary Link Test {}'.format(n))
    text = factory.sequence(lambda n: 'Summary Link Test {}'.format(n))
    image_url = factory.sequence(lambda n: 'Summary Link Test {}'.format(n))


class CommentFactory(factory.DjangoModelFactory):
    class Meta:
        model = Comment

    owner = factory.SubFactory(AccountFactory)
    post = factory.SubFactory(PostFactory)


class ReactionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Reaction

    owner = factory.SubFactory(AccountFactory)
    post = factory.SubFactory(PostFactory)
