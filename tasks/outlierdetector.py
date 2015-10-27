import time
import numpy as np
from settings import settings
from model.persistence import AerospikeSession
from datetime import datetime
from scipy.stats import multivariate_normal
from tasks.generictask import GenericTask
from model.example import Example
from model.prediction import Prediction


class OutlierDetector(GenericTask):

    page_size = 1000
    limit = None
    allowed_kwargs = [
        'project',
        'logger',
        'interval',
    ]

    def _before(self, *args, **kwargs):
        self.init_t = time.time()
        self.session = AerospikeSession(**settings['aerospike'])

    def density(self, X):
        mean = np.mean(X, 0)
        sigma2 = np.var(X, 0)
        cov = np.diag(sigma2)
        return multivariate_normal.pdf(X, mean=mean, cov=cov)

    def find_outliers(self, X, p, epsilons):
        outliers = []
        for k, e in enumerate(epsilons):
            outliers.insert(k, X[p < e, :].shape[0])
        return (outliers, epsilons)

    def execute(self, *args, **kwargs):
        """Run outlier detection table
        """


        project_interval = "{0}_{1}".format(
            self.project.full_name, self.interval)

        t1 = time.time()
        labels, X = self.create_ndarray(
            self.session.query(Example).filter_by(p_interval=project_interval)
            # self.session.query(Example).filter_by(ip_address='84.120.211.34')
        )
        t2 = time.time()
        np.random.shuffle(X)

        # multivariate gauss
        t3 = time.time()
        columns = ['status_200', 'as_bot', 'as_badbot']
        columns_idx = []
        for c in columns:
            columns_idx.append(labels.index(c))

        p = self.density(X[:, columns_idx])
        t4 = time.time()
        outliers, epsilon = self.find_outliers(X, p, self.project.list_epsilons)
        t5 = time.time()

        self.logger.info("\tDimensions are {0}".format(X.shape))
        self.logger.info("\t{0}MB used in data".format(X.nbytes/1024/1024))
        self.logger.info("\tshuffle done ({0:.3f}s):".format(t3-t2))
        self.logger.info("\tmultivariate done ({0:.3f}s):".format(t4-t3))
        self.logger.info("\tfind outliers done ({0:.3f}s):".format(t5-t4))

        # TAKE CARE, loop function not vectorized internally
        Xp = np.c_[X, p]
        for x in Xp:
            if x[-1] < self.project.cur_epsilon:
                prediction = Prediction({
                    'interval': self.interval,
                    'ip_address': self.int2ip(int(x[labels.index('ip_address')])),
                    'period': x[labels.index('period')],
                    'model': 'gauss_multivariate',
                    'project': self.project.full_name,
                    'epsilon': float(self.project.cur_epsilon),
                    'pvalue': float(x[-1])
                })
                self.session.add(prediction)


    def create_ndarray(self, resultset):
        """ Create a numpy ndarray with aerospike results via
            fromitem + data_generator. Returns labels and data separated.
        """
        labels = self.labels(resultset.first())
        X = np.fromiter(
            self.data_generator(resultset),
            np.uint32
        ).reshape([-1, len(labels)])
        return (labels, X)

    def data_generator(self, examples):
        """ Generator that returns each field of each example for filling
            numpy ndarray. Be aware of types because numpy ndarray must have
            all items of same dtype.
        """
        for example in examples:
            yield example.period
            yield example.interval
            yield self.ip2int(example.ip_address)
            for name, value in example._custom_data.items():
                if isinstance(value, (int)):
                    yield value

    def labels(self, example):
        """ Return all labels of an example. Numpy array has no labels,
            we manage in separate list (same order). If something change here
            must change in data_generator and viceversa.
        """
        labels = ['period', 'interval', 'ip_address']
        for name, value in example._custom_data.items():
            if isinstance(value, (int)):
                labels.append(name)
        return labels

    def ip2int(self, s):
        "Convert dotted IPv4 address to integer."
        return reduce(lambda a, b: a << 8 | b, map(int, s.split(".")))


    def int2ip(self, ip):
        "Convert 32-bit integer to dotted IPv4 address."
        return ".".join(map(lambda n: str(ip >> n & 0xFF), [24, 16, 8, 0]))