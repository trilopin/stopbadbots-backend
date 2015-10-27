from nose.tools import eq_, ok_, assert_raises
from schematics.exceptions import ModelValidationError
from model.user import User
import uuid
import datetime
import six


class TestUser:

    def setup(self):
        pass

    def teardown(self):
        pass

    @classmethod
    def setup_class(cls):
        cls.minimum_data = {
            'name': 'alias',
            'email': 'user@example.com'
        }
        cls.complete_data = {
            'name': 'alias',
            'complete_name': u'User name',
            'email': 'user@example.com',
            'salt': uuid.uuid4(),
            'private_token': uuid.uuid4(),
            'password': 'secret',
        }
    @classmethod
    def teardown_class(cls):
        pass

    def test_init(self):
        pass

    def test_create_minimum_data(self):
        user = User(self.minimum_data)
        eq_('alias', user.name)
        eq_('user@example.com', user.email)
        ok_(isinstance(user.salt, uuid.UUID))
        ok_(isinstance(user.private_token, uuid.UUID))
        ok_(isinstance(user.created_ts, int))
        if six.PY2:
            ok_(isinstance(user.password, unicode))
        if six.PY3:
            ok_(isinstance(user.password, str))

    def test_create_complete(self):
        user = User(self.complete_data)
        eq_('alias', user.name)
        eq_('User name', user.complete_name)
        eq_('user@example.com', user.email)
        ok_(isinstance(user.salt, uuid.UUID))
        ok_(isinstance(user.private_token, uuid.UUID))
        ok_(isinstance(user.created_ts, int))
        if six.PY2:
            ok_(isinstance(user.password, unicode))
        if six.PY3:
            ok_(isinstance(user.password, str))

    def test_key(self):
        user = User(self.minimum_data)
        eq_('alias', user.__key__)

    def test_tablename(self):
        eq_('user', User.__tablename__)
        user = User()
        eq_('user', user.__tablename__)

    def test_validate_minimum_data(self):
        user = User(self.minimum_data)
        user.validate()

    def test_validate_complete(self):
        user = User(self.complete_data)
        user.validate()

    def test_validate_fails(self):
        user = User(self.complete_data)
        user.email = 'fake'
        user.private_token = 'fake'
        user.auth_token = 'fake'
        user.salt = 'fake'

        with assert_raises(ModelValidationError) as cm:
            user.validate()

        ok_('email' in cm.exception.messages.keys())
        ok_('private_token' in cm.exception.messages.keys())
        ok_('auth_token' in cm.exception.messages.keys())
        ok_('salt' in cm.exception.messages.keys())

    def test_to_native(self):
        user = User(self.complete_data)
        native = user.to_native()
        ok_(isinstance(native, dict))
        eq_('alias', user['name'])
        eq_('User name', user['complete_name'])
        eq_('user@example.com', user['email'])
        ok_(isinstance(user['salt'], uuid.UUID))
        ok_(isinstance(user['private_token'], uuid.UUID))
        ok_(isinstance(user['created_ts'], int))
        if six.PY2:
            ok_(isinstance(user['password'], unicode))
        if six.PY3:
            ok_(isinstance(user['password'], str))

    def test_makecheck_password(self):
        user = User(self.complete_data)
        password = user.make_password('secret')
        ok_(isinstance(password, str))
        ok_(len(password) > 10)
        eq_('secret', user.password)  # still not changed
        user.password = password
        ok_(user.check_password('secret'))
