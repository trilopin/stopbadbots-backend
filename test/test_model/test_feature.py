from nose.tools import eq_, ok_, assert_raises
from model.feature import Feature
import datetime

class TestFeature:

    def setup(self):
        pass

    def teardown(self):
        pass

    @classmethod
    def setup_class(cls):
        cls.minimum_data = {
            'project': 'alias/project',
            'name': 'status_200',
        }

        cls.additional_data = {
            'min30': 0.0,
            'mean30': 0.0453,
            'max30': 1119.0,
            'var30': 28.5136,
            'std30': 5.3398,
            'median30': 0.0,
        }

    @classmethod
    def teardown_class(cls):
        pass

    def test_init(self):
        pass

    def test_create_minimum_data(self):
        feature = Feature(self.minimum_data)
        eq_('alias/project', feature.project)
        eq_('status_200', feature.name)

    def test_create_complete(self):
        feature = Feature(self.minimum_data)
        feature.add_custom_data(self.additional_data)
        eq_('alias/project', feature.project)
        eq_('status_200', feature.name)
        eq_(0.0, feature.min30)
        eq_(0.0453, feature.mean30)
        eq_(1119.0, feature.max30)
        eq_(28.5136, feature.var30)
        eq_(5.3398, feature.std30)
        eq_(0.0, feature.median30)


    def test_key(self):
        feature = Feature(self.minimum_data)
        eq_('alias/project-status_200', feature.__key__)

    def test_tablename(self):
        eq_('feature', Feature.__tablename__)
        feature = Feature(self.minimum_data)
        eq_('feature', feature.__tablename__)

    def test_validate_minimum_data(self):
        feature = Feature(self.minimum_data)
        feature.validate()

    def test_validate_complete_data(self):
        feature = Feature(self.minimum_data)
        feature.add_custom_data(self.additional_data)
        feature.validate()

    def test_to_primitive(self):
        feature = Feature(self.minimum_data)
        feature.add_custom_data(self.additional_data)
        primitive = feature.to_primitive()
