import factory

from account.factories import AccountFactory
from link.models import Post, Comment, Reaction


class PostFactory(factory.DjangoModelFactory):
    class Meta:
        model = Post

    owner = factory.SubFactory(AccountFactory)
    publisher = factory.SubFactory(AccountFactory)


class CommentFactory(factory.DjangoModelFactory):
    class Meta:
        model = Comment

    owner = factory.SubFactory(AccountFactory)
    post = factory.SubFactory(PostFactory)


class Reaction(factory.DjangoModelFactory):
    class Meta:
        model: Reaction

    owner = factory.SubFactory(AccountFactory)
    post = factory.SubFactory(PostFactory)