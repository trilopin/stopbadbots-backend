

class GenericTask(object):
    allowed_kwargs = []

    def __init__(self, *args, **kwargs):
        for k in kwargs.keys():
            if k in self.allowed_kwargs:
                self.__setattr__(k, kwargs[k])

    def _before(self, *args, **kwargs):
        pass

    def _after(self, *args, **kwargs):
        pass

    def run(self, *args, **kwargs):
        self._before(*args, **kwargs)
        self.execute(*args, **kwargs)
        self._after(*args, **kwargs)
