from nose.tools import eq_, ok_, assert_raises
from model.prediction import Prediction
import datetime

class TestPrediction:

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
            'model': 'gaussian_multivariate'
        }

        cls.additional_data = {
            'pvalue': 1e-35,
            'epsilon': 2e-31,
            'label': 'outlier',
        }

    @classmethod
    def teardown_class(cls):
        pass

    def test_init(self):
        pass

    def test_create_minimum_data(self):
        prediction = Prediction(self.minimum_data)
        eq_(15, prediction.interval)
        eq_('alias/project', prediction.project)
        eq_('8.8.8.8', prediction.ip_address)
        eq_(1415823240, prediction.period)
        eq_('gaussian_multivariate', prediction.model)

    def test_create_complete(self):
        prediction = Prediction(self.minimum_data)
        prediction.add_custom_data(self.additional_data)
        eq_(15, prediction.interval)
        eq_('alias/project', prediction.project)
        eq_('8.8.8.8', prediction.ip_address)
        eq_(1415823240, prediction.period)
        eq_('gaussian_multivariate', prediction.model)
        eq_(1e-35, prediction.pvalue)
        eq_(2e-31, prediction.epsilon)
        eq_('outlier', prediction.label)


    def test_key(self):
        prediction = Prediction(self.minimum_data)
        eq_('alias/project-15-1415823240-8.8.8.8-gaussian_multivariate', prediction.__key__)

    def test_tablename(self):
        eq_('prediction', Prediction.__tablename__)
        prediction = Prediction(self.minimum_data)
        eq_('prediction', prediction.__tablename__)

    def test_validate_minimum_data(self):
        prediction = Prediction(self.minimum_data)
        prediction.validate()

    def test_validate_complete_data(self):
        prediction = Prediction(self.minimum_data)
        prediction.add_custom_data(self.additional_data)
        prediction.validate()

    def test_to_primitive(self):
        prediction = Prediction(self.minimum_data)
        prediction.add_custom_data(self.additional_data)
        primitive = prediction.to_primitive()
