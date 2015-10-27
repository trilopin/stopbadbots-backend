
from nose.tools import eq_, ok_, assert_raises
import six
import view.auth
import falcon
if six.PY3:
    from unittest.mock import Mock, MagicMock, patch
if six.PY2:
    from mock import Mock, MagicMock, patch

class TestAuthView:

    def setup(self):
        self.config = {}
        self.view = view.auth.Authentication(self.config)
        self.res = Mock()
        self.req = MagicMock()

    def teardown(self):
        pass

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def set_data(self, data):
        self.req.context = {'doc': data}


    def test_on_options(self):
        self.res.set_header = Mock()
        self.view.on_options(self.req, self.res)
        self.res.set_header.assert_called_once_with('Allow', 'OPTIONS, POST')



    def test_on_post_private_token_fails(self):
        #setup data
        self.set_data({'private_token': '180e0f54-076e-4a3f-a1bb-a557b0868f5d'})

        #setup mocks
        User = Mock()
        self.view._model = Mock(return_value=User)
        User.get = Mock(side_effect=Exception)

        with assert_raises(falcon.HTTPForbidden):
            self.view.on_post(self.req, self.res)


    @patch('uuid.uuid4')
    def test_on_post_private_token(self, uuid_mock):
        #setup data
        self.set_data({'private_token': '180e0f54-076e-4a3f-a1bb-a557b0868f5d'})

        #setup mocks
        User = Mock()
        user = Mock()
        self.view._model = Mock(return_value=User)
        User.get = Mock(return_value=user)
        user.ttl = Mock(return_value=user)
        user.update = Mock(return_value=user)
        uuid_mock.return_value = '<TOKEN-UUID>'

        #action
        self.view.on_post(self.req, self.res)

        #assertions
        User.get.assert_called_once_with(private_token='180e0f54-076e-4a3f-a1bb-a557b0868f5d')
        user.ttl.assert_called_once_with(3600)
        user.update.assert_called_once_with(auth_token='<TOKEN-UUID>')


    def test_on_post_name_fails_beacause_no_password(self):
        #setup data
        self.set_data({'name': 'user'})

        #setup mocks
        User = Mock()
        user = Mock()
        self.view._model = Mock(return_value=User)
        User.get = Mock(return_value=user)

        #action
        with assert_raises(falcon.HTTPBadRequest):
            self.view.on_post(self.req, self.res)

        #assertions
        User.get.assert_called_once_with(name='user')

    def test_on_post_wrong_data(self):
        #setup data
        self.set_data({'another': 'value'})

        #action
        with assert_raises(falcon.HTTPBadRequest):
            self.view.on_post(self.req, self.res)



    def test_on_post_name_password_fails(self):
        #setup data
        self.set_data({'name': 'user', 'password': 'secret'})

        #setup mocks
        User = Mock()
        user = Mock()
        self.view._model = Mock(return_value=User)
        User.get = Mock(return_value=user)
        user.ttl = Mock(return_value=user)
        user.password = 'hashed-secret'
        user.make_password = Mock(return_value='different-hashed-secret')
        user.update = Mock(return_value=user)

        #action
        with assert_raises(falcon.HTTPForbidden):
            self.view.on_post(self.req, self.res)

        #assertions
        User.get.assert_called_once_with(name='user')
        user.make_password.assert_called_once_with('secret')




    @patch('uuid.uuid4')
    def test_on_post_name_password(self, uuid_mock):
        #setup data
        self.set_data({'name': 'user', 'password': 'secret'})

        #setup mocks
        User = Mock()
        user = Mock()
        self.view._model = Mock(return_value=User)
        User.get = Mock(return_value=user)
        user.ttl = Mock(return_value=user)
        user.password = 'hashed-secret'
        user.make_password = Mock(return_value='hashed-secret')
        user.update = Mock(return_value=user)
        uuid_mock.return_value = '<TOKEN-UUID>'

        #action
        self.view.on_post(self.req, self.res)

        #assertions
        User.get.assert_called_once_with(name='user')
        user.make_password.assert_called_once_with('secret')
        user.ttl.assert_called_once_with(3600)
        user.update.assert_called_once_with(auth_token='<TOKEN-UUID>')
