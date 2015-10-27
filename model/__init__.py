from schematics.models import Model


class SbbModel(Model):

    __abstract__ = True
    __tablename__ = None


    def __init__(self, raw_data=None, deserialize_mapping=None, strict=True):
        self._custom_data = {}
        pure_data = None
        impure_data = None
        if raw_data:
            pure_data = {k: v for k, v in raw_data.items() if k in self._fields.keys()}
            impure_data = {k: v for k, v in raw_data.items() if k not in self._fields.keys()}
        super(SbbModel, self).__init__(pure_data, deserialize_mapping=deserialize_mapping, strict=strict)
        if impure_data:
            self.add_custom_data(impure_data)

    def add_custom_data(self, data):
        self._custom_data.update(data)

    def before_save(self):
        pass

    @property
    def __key__(self):
        pass

    @property
    def __namespace__(self):
        pass

    def __getattr__(self, name):
        '''
        Get custom data as regular attributes
        '''
        if name != '_custom_data' and name in self._custom_data.keys():
            return self._custom_data[name]
        else:
            raise AttributeError("{0} object has no attribute {1}".format(self.__class__, name))

    def __setattr__(self, name, value):
        '''
        Set custom data as regular attributes
        '''
        try:
            super(SbbModel, self).__setattr__(name, value)
        except AttributeError:
            self._custom_data[name] = value

    def to_primitive(self):
        regular = super(SbbModel, self).to_primitive()
        regular.update(self._custom_data)
        return regular