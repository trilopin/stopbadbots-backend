from nose.tools import eq_, ok_, assert_raises
from model.predictionmodel import PredictionModel
import datetime

class TestPredictionModel:

    def setup(self):
        pass

    def teardown(self):
        pass

    @classmethod
    def setup_class(cls):
        cls.minimum_data = {
            'project': 'alias/project',
            'name': 'mymodel',
            'interval': 30,
        }

        cls.additional_data = {
            'mean': 4.533,
            'cov': [4.5, 3, 5],
        }

    @classmethod
    def teardown_class(cls):
        pass

    def test_init(self):
        pass

    def test_create_minimum_data(self):
        predictionmodel = PredictionModel(self.minimum_data)
        eq_('alias/project', predictionmodel.project)
        eq_('mymodel', predictionmodel.name)
        eq_(30, predictionmodel.interval)
        eq_('active', predictionmodel.status)

    def test_create_complete(self):
        predictionmodel = PredictionModel(self.minimum_data)
        predictionmodel.add_custom_data(self.additional_data)
        eq_('alias/project', predictionmodel.project)
        eq_('mymodel', predictionmodel.name)
        eq_('active', predictionmodel.status)
        eq_(30, predictionmodel.interval)
        eq_(4.533, predictionmodel.mean)
        eq_([4.5, 3, 5], predictionmodel.cov)



    def test_key(self):
        predictionmodel = PredictionModel(self.minimum_data)
        eq_('alias/project-30-mymodel', predictionmodel.__key__)

    def test_tablename(self):
        eq_('model', PredictionModel.__tablename__)
        predictionmodel = PredictionModel(self.minimum_data)
        eq_('model', predictionmodel.__tablename__)

    def test_validate_minimum_data(self):
        predictionmodel = PredictionModel(self.minimum_data)
        predictionmodel.validate()

    def test_validate_complete_data(self):
        predictionmodel = PredictionModel(self.minimum_data)
        predictionmodel.add_custom_data(self.additional_data)
        predictionmodel.validate()

    def test_to_primitive(self):
        predictionmodel = PredictionModel(self.minimum_data)
        predictionmodel.add_custom_data(self.additional_data)
        primitive = predictionmodel.to_primitive()
