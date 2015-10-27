from nose.tools import eq_, assert_raises  # , ok_,
from tasks.filetodb import FileToDb


class TestFileToDb:

    def setup(self):
        pass

    def teardown(self):
        pass

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def test_init(self):

        fakeproject = object()

        filetodb = FileToDb(
            file='file',
            interval=15,
            notexistingproperty='value',
            project=fakeproject)
        eq_(filetodb.file, 'file')
        eq_(filetodb.project, fakeproject)
        eq_(filetodb.interval, 15)
        assert_raises(AttributeError, getattr, filetodb, 'notexistingproperty')
