import factory
import hashlib

from django.contrib.auth.models import User
from meadowlark import models

class UserFactory(factory.Factory):
    FACTORY_FOR = User

    id = factory.Sequence(lambda a: int(a)+1)
    username = factory.Sequence(lambda a: 'username%d' %(int(a)+1))
    password = factory.Sequence(lambda a: 'password%d' %(int(a)+1))
    email = factory.Sequence(lambda a: 'username%d@test.com' %(int(a)+1))

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserFactory, cls)._prepare(create, **kwargs)

        if password:
            user.set_password(password)
            if create:
                user.save()

        return user

class AccessTokenFactory(factory.Factory):
    FACTORY_FOR = models.AccessToken

    user = factory.SubFactory(UserFactory)
    token = factory.Sequence(lambda a: hashlib.sha256('username%d' %(int(a) + 1)).hexdigest())

class FolderFactory(factory.Factory):
    FACTORY_FOR = models.Folder

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda a: 'folder%d' %(int(a) + 1))

class FileFactory(factory.Factory):
    FACTORY_FOR = models.File

    folder = factory.SubFactory(FolderFactory)
    name = factory.Sequence(lambda a: 'file%d' %(int(a) + 1))