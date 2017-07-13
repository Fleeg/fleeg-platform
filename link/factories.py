import factory

from link.models import Post, Comment, Reaction


class PostFactory(factory.DjangoModelFactory):
    class Meta:
        model = Post


class CommentFactory(factory.DjangoModelFactory):
    class Meta:
        model = Comment


class Reaction(factory.DjangoModelFactory):
    class Meta:
        model: Reaction

