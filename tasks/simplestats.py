import time
from datetime import datetime
from settings import settings
from model.persistence import AerospikeSession
from model.example import Example
from model.feature import Feature
from tasks.generictask import GenericTask
import numpy as np


class SimpleStats(GenericTask):

    allowed_kwargs = [
        'project',
        'interval',
        'logger'
    ]

    def _before(self, *args, **kwargs):
        self.init_t = time.time()
        self.session = AerospikeSession(**settings['aerospike'])

    def execute(self, *args, **kwargs):
        """ Computes simple statistics over all examples of project and interval.
            All operations are calculated over entire matrix across columns
            (features) except percentile and histogram. After all calculations
            data is saved in feature set in one record per feature/project and one
            bin per stat/interval.
        """
        project_interval = "{0}_{1}".format(
            self.project.full_name, self.interval)

        labels, X = self.create_ndarray(
            self.session.query(Example).filter_by(p_interval=project_interval)
        )

        tmp_stats = {
            'max': np.amax(X[:, 3:], 0),
            'min': np.amin(X[:, 3:], 0),
            'mean': np.mean(X[:, 3:], 0),
            'std': np.std(X[:, 3:], 0),
            'var': np.var(X[:, 3:], 0),
            'median': np.median(X[:, 3:], 0),
        }

        # reshape by feature
        for feature_index, feature_name in enumerate(labels[3:]):
            if feature_name == 'grouptime':
                continue
            custom_data = {}
            xkey = feature_index + 3
            feature = Feature({'project': self.project.full_name, 'name': feature_name})
            hist, bin_hedges = np.histogram(X[:, xkey], bins=10)
            # cast to list are needed by persistence layer (array not supported)
            custom_data['histogram{0}'.format(self.interval)] = [list(hist), list(bin_hedges)]
            custom_data['percentile{0}'.format(self.interval)] = list(np.percentile(X[:, xkey], [25, 50, 75]))

            for stat_name, stat_value in tmp_stats.items():
                name = '{0}{1}'.format(stat_name, self.interval)
                value = float(stat_value[feature_index]) # cast needed
                custom_data[name] = value
            feature.add_custom_data(custom_data)
            self.session.add(feature)

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