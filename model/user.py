import os
import uuid
import hashlib
from schematics.types import StringType, UUIDType, EmailType, IntType
from model import SbbModel
import time
import six


def initial_password():
    if six.PY2:
        return os.urandom(15).decode('latin1')
    if six.PY3:
        return str(os.urandom(15))


class User(SbbModel):
    __tablename__ = 'user'
    name = StringType(required=True)
    complete_name = StringType()
    email = EmailType(required=True)
    salt = UUIDType(required=True, default=uuid.uuid4)
    password = StringType(required=True, default=initial_password)
    created_ts = IntType(required=True, default=time.time)
    private_token = UUIDType(required=True, default=uuid.uuid4)
    auth_token = UUIDType()

    @property
    def __key__(self):
        return self.name

    @property
    def __namespace__(self):
        return None

    def check_password(self, clear_password):
        return self.make_password(clear_password) == self.password

    def make_password(self, clear_password):
        if six.PY2:
            return  hashlib.sha256(
                       clear_password + str(self.salt)
                    ).hexdigest()
        if six.PY3:
            return  hashlib.sha256(
                       bytes(clear_password, 'utf-8') + bytes(str(self.salt), 'utf-8')
                    ).hexdigest()

    # def new_project(self, **kwargs):
    #     kwargs['user'] = self.name
    #     project = Project.if_not_exists().create(**kwargs)
    #     return project

    # def new_host(self, **kwargs):
    #     kwargs['user'] = self.name
    #     host = Host.if_not_exists().create(**kwargs)
    #     return host

    # @property
    # def projects(self):
    #     if not hasattr(self, '_projects'):
    #         self._projects = Project.objects(user=self.name).allow_filtering()
    #     return self._projects


class Auth(SbbModel):
    __tablename__ = 'auth'
    user = StringType(required=True)
    token = UUIDType(required=True, default=uuid.uuid4)

    @property
    def __key__(self):
        return self.user

    @property
    def __namespace__(self):
        return None
