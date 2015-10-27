import aerospike


class AerospikeSession(object):

    def __init__(self, **kwargs):
        self.namespace = kwargs['namespace']
        config = {
            'hosts': kwargs['hosts']
        }
        self.aerospike = aerospike.client(config).connect()

    def add(self, model, meta=None):
        model.before_save()
        model.validate()
        key = (self.namespace, model.__tablename__, model.__key__)
        bins = {k: v for k, v in model.to_primitive().items() if v is not None}
        return self.aerospike.put(key, bins, meta)

    def exists(self, model):
        key = (self.namespace, model.__tablename__, model.__key__)
        return self.aerospike.exists(key)


    def query(self, model, **kwargs):
        return AerospikeQuery(self.aerospike, model, self.namespace, kwargs)


class AerospikeQuery(object):
    def __init__(self, session, model, namespace, kwargs):
        self.session = session
        self.model = model
        self.namespace = namespace
        self.tablename = model.__tablename__

    def filter_by(self, callback=None, **kwargs):
        self.query = self.session.query(self.namespace, self.tablename)
        if len(kwargs) != 1:
            raise ValueError('only one filter is allowed')
        for name, value in kwargs.items():
            self.query.where(aerospike.predicates.equals(name, value))
        if callback is None:
            results = self.query.results()
            return AerospikeDataSet(self.model, results)
        else:
            self.query.foreach(callback)

    def apply_filter_by(self, udf, callback=None, **kwargs):
        def print_simple(record):
            print(record)

        self.query = self.session.query(self.namespace, self.tablename)
        if len(kwargs) != 1:
            raise ValueError('only one filter is allowed')
        for name, value in kwargs.items():
            self.query.where(aerospike.predicates.equals(name, value))
        self.query.apply(udf['module'], udf['function'], udf['args'])
        if callback is None:
            results = self.query.results()
            return AerospikeDataSet(self.model, results)
        else:
            self.query.foreach(callback)

    def get(self, primary_key):
        key = (self.namespace, self.tablename, primary_key)
        (key, meta, bins) = self.session.get(key)
        return self.model(bins)


class AerospikeDataSet(object):
    def __init__(self, model, data):
        self.model = model
        self.data = data
        self.current = 0

    def __iter__(self):
        return self

    def next(self):
        if self.current < len(self.data):
            (key, meta, bins) = self.data[self.current]
            self.current += 1
            return self.model(bins)
        else:
            raise StopIteration()

    def first(self):
        if len(self.data)>0:
            (key, meta, bins) = self.data[0]
            return self.model(bins)
        else:
            raise ValueError('Empty dataset called with first')



# self.aerospike.query(User).where(auth_token=token)