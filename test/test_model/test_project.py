from nose.tools import eq_, ok_, assert_raises
from schematics.exceptions import ModelValidationError, ModelConversionError
from model.project import Project
import datetime



class TestProject:

    def setup(self):
        pass

    def teardown(self):
        pass

    @classmethod
    def setup_class(cls):
        cls.minimum_data = {
            'user': 'alias',
            'name': 'project',
            'logdir': '/dir/to/logs',
            'logpattern': '*.log',
            'logformat': 'ApacheCombinedFormat',
        }
        cls.complete_data = {
            'user': 'alias',
            'name': 'project',
            'logdir': '/dir/to/logs',
            'logpattern': '*.log',
            'interval': [15, 30, 45],
            'collector': 'MyCollector',
            'hosts': ['host1', 'host2'],
            'whitelist': {
                "bingbot2": "157.57.0.0/16",
                "googlebot": "66.249.0.0/16",
                "bingbot": "157.55.0.0/16"
            },
            'logformat': 'MyFormat',
            'custom': {'key': 'value'},
            'cur_epsilon': 1e-8,
            'list_epsilons': [1e-9, 1e-10, 1e-8],
        }
        cls.wrong_data = {
            'user': 5,
            'name': 9,
            'bucket': 1,
            'logdir': 4.4,
            'logpattern': 2,
            'interval': '15',
            'collector': 0,
            'hosts': '127.0.0.1',
            'whitelist': 'google',
            'logformat': 1,
            'custom': 33,
            'cur_epsilon': 'epsilon',
            'list_epsilons': 1e-9,
        }

    @classmethod
    def teardown_class(cls):
        pass

    def test_init(self):
        pass

    def test_create_minimum_data(self):
        project = Project(self.minimum_data)
        eq_('alias', project.user)
        eq_('project', project.name)
        eq_('*.log', project.logpattern)
        eq_('ApacheCombinedFormat', project.logformat)
        eq_('/dir/to/logs', project.logdir)
        eq_([30, 360, 720, 1440], project.interval)
        eq_('HttpCollector', project.collector)
        eq_(None, project.hosts)
        eq_(None, project.whitelist)
        eq_(None, project.custom)
        eq_(None, project.cur_epsilon)
        ok_(isinstance(project.list_epsilons,list))
        eq_(101, len(project.list_epsilons))
        ok_(isinstance(project.created_ts, int))


    def test_create_complete(self):
        project = Project(self.complete_data)
        eq_('alias', project.user)
        eq_('project', project.name)
        eq_('*.log', project.logpattern)
        eq_('MyFormat', project.logformat)
        eq_('/dir/to/logs', project.logdir)
        eq_([15, 30, 45], project.interval)
        eq_('MyCollector', project.collector)
        eq_(['host1', 'host2'], project.hosts)
        eq_({
                "bingbot2": "157.57.0.0/16",
                "googlebot": "66.249.0.0/16",
                "bingbot": "157.55.0.0/16"
            }, project.whitelist)
        eq_({'key': 'value'}, project.custom)
        eq_(1e-8, project.cur_epsilon)
        eq_([1e-9, 1e-10, 1e-8], project.list_epsilons)
        ok_(isinstance(project.created_ts, int))

    def test_create_fails_bad_types_data(self):
        with assert_raises(ModelConversionError) as cm:
            Project(self.wrong_data)
        eq_(4, len(cm.exception.messages.keys()))

    def test_key(self):
        project = Project(self.minimum_data)
        eq_('alias/project', project.__key__)

    def test_tablename(self):
        eq_('project', Project.__tablename__)
        project = Project()
        eq_('project', project.__tablename__)

    def test_validate_minimum_data(self):
        project = Project(self.minimum_data)
        project.validate()

    def test_validate_complete(self):
        project = Project(self.complete_data)
        project.validate()

    def test_before_save(self):
        project = Project(self.complete_data)
        project.cur_epsilon = None
        project.before_save()
        eq_([1e-10, 1e-9, 1e-8], project.list_epsilons)
        eq_(1e-9, project.cur_epsilon)


    def test_validate_fails_no_data(self):
        project = Project()
        with assert_raises(ModelValidationError) as cm:
            project.validate()
        eq_(5, len(cm.exception.messages.keys()))


    def primitive(self):
        project = Project(self.complete_data)
        primitive = project.to_primitive()
        ok_(isinstance(primitive, dict))
        eq_('project', primitive['name'])
        eq_('alias', primitive['user'])
        eq_('*.log', primitive['logpattern'])
        eq_('MyFormat', primitive['logformat'])
        eq_('/dir/to/logs', primitive['logdir'])
        eq_([15, 30, 45], primitive['interval'])
        eq_('MyCollector', primitive['collector'])
        eq_(['host1', 'host2'], primitive['hosts'])
        eq_({
                "bingbot2": "157.57.0.0/16",
                "googlebot": "66.249.0.0/16",
                "bingbot": "157.55.0.0/16"
            }, primitive['whitelist'])
        eq_({'key': 'value'}, primitive['custom'])
        eq_(1e-8, primitive['cur_epsilon'])
        eq_([1e-9, 1e-10, 1e-8], primitive['list_epsilons'])
        ok_(isinstance(primitive['created_ts'], int))
