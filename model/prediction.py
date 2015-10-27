from model import SbbModel
from schematics.types import IntType, IPv4Type, StringType
import datetime
import time


class Prediction(SbbModel):
    __tablename__ = 'prediction'

    project = StringType(required=True)
    interval = IntType(required=True)
    period = IntType(required=True)
    ip_address = IPv4Type(required=True)
    model = StringType(required=True)
    pi_model = StringType()  # fake property for indexing
    created_at = IntType()

    @property
    def __key__(self):
        return "{0}-{1}-{2}-{3}-{4}".format(
            self.project, self.interval, self.period, self.ip_address, self.model)

    @property
    def __namespace__(self):
        return None

    @property
    def period_dt(self):
        return datetime.datetime.fromtimestamp(self.period)

    def before_save(self):
        self.pi_model = "{0}_{1}_{2}".format(self.project, self.interval, self.model)
        self.created_at = int(time.time())

