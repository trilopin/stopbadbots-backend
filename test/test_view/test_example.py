from nose.tools import eq_, ok_, assert_raises
import view.example
import falcon
import os
import six
if six.PY3:
    from unittest.mock import Mock, MagicMock, patch
if six.PY2:
    from mock import Mock, MagicMock, patch
class TestExampleCollectionView:

    def setup(self):
        self.config = {}
        self.view = view.example.Collection(self.config)
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


@patch('os.remove')
@patch('database.keyspace')
def test_process_data(keyspace_mock, remove_mock):
    filename = os.path.abspath(os.path.dirname(__file__)) \
               + "/fixture/tempfile_plain.txt"
    project = Mock()
    project.name = 'projectname'
    model = Mock()
    model.fill_data = Mock()
    model.save = Mock()

    view.example.process_data(filename, None, 15, project, model)

    keyspace_mock.assert_called_once_with('projectname')
    remove_mock.assert_called_once_with(filename)
    eq_(model.call_count, 9)
    eq_(len(model.mock_calls), 27) # 9x model + 9x filldata + 9x save
    model.assert_has_calls([call(ip_address=ANY, example_time=ANY)])
    model.assert_has_calls([call().fill_data(ANY, ANY)])
    model.assert_has_calls([call().save()])
