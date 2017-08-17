import factory

from django.contrib.auth.models import User
from account.models import Account, Relationship


DEFAULT_PASSWORD = 'abc@123'


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.sequence(lambda n: 'user{}'.format(n))
    email = factory.lazy_attribute(lambda n: '{}@test.com'.format(n.username.lower()))
    password = factory.PostGenerationMethodCall('set_password', DEFAULT_PASSWORD)
    first_name = factory.sequence(lambda n: 'First User Name {}'.format(n))
    last_name = factory.sequence(lambda n: 'Last User Name {}'.format(n))


class AccountFactory(factory.DjangoModelFactory):
    class Meta:
        model = Account

    user = factory.SubFactory(UserFactory)


class RelationshipFactory(factory.DjangoModelFactory):
    class Meta:
        model = Relationship

    owner = factory.SubFactory(AccountFactory)
    follow = factory.SubFactory(AccountFactory)
