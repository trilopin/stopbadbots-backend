from model import SbbModel
from schematics.types import IntType, IPv4Type, StringType
import datetime
import copy


class Example(SbbModel):
    __tablename__ = 'example'

    project = StringType(required=True)
    interval = IntType(required=True)
    p_interval = StringType()  # fake property for indexing
    period = IntType(required=True)
    ip_address = IPv4Type(required=True)

    @property
    def __key__(self):
        return "{0}-{1}-{2}-{3}".format(
            self.project, self.interval, self.period, self.ip_address)

    @property
    def __namespace__(self):
        return None

    @property
    def period_dt(self):
        return datetime.datetime.fromtimestamp(self.period)

    def before_save(self):
        self.p_interval = "{0}_{1}".format(self.project, self.interval)

    def reduce_interval(self, new_interval):
        if new_interval > 24*60:
            raise ValueError('Maximum interval allowed is 1440 minutes (1 day)')
        period = datetime.datetime.fromtimestamp(self.period)
        diff = ((period.minute + period.hour * 60) * 60) % (new_interval*60)
        self.period = self.period - diff
        self.interval = new_interval

    def __add__(self, other):
        if not isinstance(other, Example):
            raise ValueError
        new_example = copy.copy(self)
        for key, value in other._custom_data.items():
            if key in self._custom_data:
                if isinstance(value, (int, float)):
                    new_example._custom_data[key] += value
        return new_example
