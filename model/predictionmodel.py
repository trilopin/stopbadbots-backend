from model import SbbModel
from schematics.types import IntType, StringType
import datetime
import time


class PredictionModel(SbbModel):
    __tablename__ = 'model'

    project = StringType(required=True)
    interval = IntType(required=True)
    status = StringType(default='active')
    name = StringType(required=True)

    @property
    def __key__(self):
        return "{0}-{1}-{2}".format(
            self.project, self.interval, self.name)

    @property
    def __namespace__(self):
        return None

    @property
    def period_dt(self):
        return datetime.datetime.fromtimestamp(self.period)

    def before_save(self):
        self.pi_model = "{0}_{1}_{2}".format(self.project, self.interval, self.model)
        self.created_at = int(time.time())

