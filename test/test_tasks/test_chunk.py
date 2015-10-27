import os
import os.path
import shutil
import uuid
from nose.tools import eq_, assert_raises, ok_
from tasks.chunk import Chunk
from model.example import Example
from model.outlier import Outlier
from model.event import Event
import six
if six.PY2:
    from mock import Mock
if six.PY3:
    from unittest.mock import Mock
CELERY_ALWAYS_EAGER = True


class TestChunk:

    def setup(self):
        pass

    def teardown(self):
        pass

    @classmethod
    def setup_class(cls):
        cls.data_dir = os.path.dirname(__file__) + '/../data/'
        ip = '127.0.0.1'



    @classmethod
    def teardown_class(cls):
        pass

    def _file_len(self, full_path):
        """ Count number of lines in a file."""
        f = open(full_path)
        nr_of_lines = sum(1 for line in f)
        f.close()
        return nr_of_lines

    def test_init(self):

        project = Mock()
        project.name = "test_project"
        project.user = "test_user"

        chunk = Chunk(
            file='file',
            compress=None,
            interval=15,
            notexistingproperty='value',
            project=project)

        eq_(chunk.file, 'file')
        eq_(chunk.compress, None)
        eq_(chunk.project, project)
        eq_(chunk.interval, 15)
        assert_raises(AttributeError, getattr, chunk, 'notexistingproperty')

    def test_run(self):
        project = Mock()
        project.name = "test_project"
        project.user = "test_user"

        filename = '/tmp/' + str(uuid.uuid4())
        shutil.copyfile(self.data_dir + '/interval15_1k.csv', filename)

        process_file_mock = Mock()
        reduce_interval_mock = Mock()

        chunk = Chunk(
            file=filename,
            logger=Mock(),
            compress=None,
            interval=15,
            process_file=process_file_mock,
            reduce_interval=reduce_interval_mock,
            project=project)
        chunk._chain_tasks = Mock()
        chunk.chunk_size = 100  # reduce chunk size for testing
        chunk.run()

        # events = Event \
        #     .objects(user=project.user, project=project.name) \
        #     .allow_filtering().all()
        # print(events[0])

        ok_(not os.path.exists(filename), 'Original file should be deleted')
        for i in range(1, 11):
            filename_part = '{0}-part{1:03d}'.format(filename, i)
            ok_(
                os.path.exists(filename_part),
                'File part {0} does not exists'.format(i))
            eq_(
                self._file_len(filename_part), chunk.chunk_size+1,
                'File part {0} does fit in {1} size'.format(i, Chunk.chunk_size))
            os.remove(filename_part)

        eq_(1, chunk._chain_tasks.call_count)
