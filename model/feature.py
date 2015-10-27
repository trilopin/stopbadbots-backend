from model import SbbModel
from schematics.types import StringType


class Feature(SbbModel):
    __tablename__ = 'feature'

    project = StringType(required=True)
    name = StringType(required=True)


    @property
    def __key__(self):
        return "{0}-{1}".format(
            self.project, self.name)

    @property
    def __namespace__(self):
        return None

