from schematics.types import StringType, IntType, FloatType
from schematics.types.compound import ListType, DictType
from schematics.exceptions import ValidationError
import time
from model import SbbModel


def default_interval():
    return [30, 360, 720, 1440]


def default_outlier_epsilons():
    epsilons = [1e-35]
    for i in range(100):
        epsilons.append(epsilons[i-1]*2)
    return epsilons


class Project(SbbModel):
    __tablename__ = 'project'
    user = StringType(required=True)  # user.name
    name = StringType(required=True)
    full_name = StringType()
    logformat = StringType(required=True)
    collector = StringType(required=True, default='HttpCollector')
    logdir = StringType(required=True)
    logpattern = StringType(required=True)
    interval = ListType(IntType(), default=default_interval)
    hosts = ListType(StringType())
    whitelist = DictType(StringType())
    custom = DictType(StringType())
    data_spec = ListType(StringType())
    list_epsilons = ListType(FloatType(), default=default_outlier_epsilons)
    cur_epsilon = FloatType()
    created_ts = IntType(default=time.time)

    @property
    def __key__(self):
        return "{0}/{1}".format(self.user, self.name)

    @property
    def __namespace__(self):
        return None

    def before_save(self):
        self.list_epsilons.sort()
        self.full_name = self.user + '/' + self.name

        # choose value for current epsilon if not set
        if self.cur_epsilon is None:
            self.cur_epsilon = self.list_epsilons[int(len(self.list_epsilons)/2)]
        if self.cur_epsilon not in self.list_epsilons:
            raise ValidationError('current epsilon is not in epsilons list')
