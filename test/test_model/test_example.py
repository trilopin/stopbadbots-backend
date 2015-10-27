from nose.tools import eq_, ok_, assert_raises
from model.example import Example
import datetime

class TestExample:

    def setup(self):
        pass

    def teardown(self):
        pass

    @classmethod
    def setup_class(cls):
        dt_epoch = datetime.datetime(1970, 1, 1, 1, 1, 0)
        cls.minimum_data = {
            'project': 'alias/project',
            'interval': 15,
            'period': (datetime.datetime(2014, 11, 12, 21, 15, 00) - dt_epoch).total_seconds(),
            'ip_address': '8.8.8.8',
        }

        cls.additional_data = {
            'param1': 1,
            'param2': 2.3,
            'param3': 1e-200,
            'param4': ['1', '2', '3'],
            'param5': {'1': 'val1', '2': 'val2'},
        }

    @classmethod
    def teardown_class(cls):
        pass

    def test_init(self):
        pass

    def test_create_minimum_data(self):
        example = Example(self.minimum_data)
        eq_(15, example.interval)
        eq_('alias/project', example.project)
        eq_('8.8.8.8', example.ip_address)
        eq_(1415823240, example.period)

    def test_create_complete(self):
        example = Example(self.minimum_data)
        example.add_custom_data(self.additional_data)
        eq_(15, example.interval)
        eq_('alias/project', example.project)
        eq_('8.8.8.8', example.ip_address)
        eq_(1415823240, example.period)
        eq_(1, example.param1)
        eq_(2.3, example.param2)
        eq_(1e-200, example.param3)
        eq_(['1', '2', '3'], example.param4)
        eq_({'1': 'val1', '2':'val2'}, example.param5)

    def test_key(self):
        example = Example(self.minimum_data)
        eq_('alias/project-15-1415823240-8.8.8.8', example.__key__)

    def test_tablename(self):
        eq_('example', Example.__tablename__)
        example = Example(self.minimum_data)
        eq_('example', example.__tablename__)

    def test_validate_minimum_data(self):
        example = Example(self.minimum_data)
        example.validate()

    def test_validate_complete_data(self):
        example = Example(self.minimum_data)
        example.add_custom_data(self.additional_data)
        example.validate()

    def test_reduce_interval(self):
        example = Example(self.minimum_data)
        example.reduce_interval(720)
        eq_(1415790000, example.period)
        eq_(datetime.datetime(2014, 11, 12, 12, 0), example.period_dt)
        eq_(720, example.interval)

        example.reduce_interval(1440)
        eq_(1415746800, example.period)
        eq_(datetime.datetime(2014, 11, 12, 0, 0), example.period_dt)
        eq_(1440, example.interval)

    def test_reduce_interval_fail(self):
        example = Example(self.minimum_data)
        with assert_raises(ValueError):
            example.reduce_interval(1500)

    def test_add(self):
        data = self.minimum_data
        data.update(self.additional_data)
        example = Example(data)
        example2 = Example(data)
        example3 = example + example2
        eq_(2, example3.param1)
        eq_(4.6, example3.param2)
        eq_(2e-200, example3.param3)
        eq_(['1', '2', '3'], example3.param4)
        eq_({'1': 'val1', '2':'val2'}, example3.param5)