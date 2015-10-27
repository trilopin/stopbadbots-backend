import os
import time
import copy
from datetime import datetime
from tasks.generictask import GenericTask
from model.example import Example
from model.persistence import AerospikeSession
from settings import settings


class FileToDb(GenericTask):

    allowed_kwargs = [
        'file',
        'interval',
        'project',
        'logger'
    ]

    def _before(self, *args, **kwargs):
        self.init_t = time.time()
        self.session = AerospikeSession(**settings['aerospike'])


    def _get_file(self):
        return open(self.file, 'rb')

    def _fix_type(self, str):
        try:
            return int(str)
        except ValueError:
            pass

        try:
            return float(str)
        except ValueError:
            pass

        return str

    def execute(self, *args, **kwargs):
        datafile = self._get_file()
        header = None
        dt_epoch = datetime(1970, 1, 1)
        common_data = {}

        for line in datafile:

            try:
                line = line.decode('utf-8')

                if header is None:
                    header = line.strip().split('\t')
                    continue

                raw_data = line.strip().split('\t')
                ip_address = '.'.join(raw_data[0:4])
                raw_data = [self._fix_type(value) for value in raw_data]
                data = dict(zip(header[4:], raw_data[4:]))
                grouptime = datetime.strptime(str(data['grouptime']), '%Y%m%d%H%M')
                grouptime_interval = grouptime - dt_epoch
                common_data = {
                    'ip_address': ip_address,
                    'interval': self.interval,
                    'project': self.project.full_name,
                    'period': int(grouptime_interval.total_seconds()),
                }
                common_data.update(data)
                example = Example(common_data)
                self.process_example(example)


            except Exception as e:
                self.logger.info(str(e))
                if 'ip_address' in common_data:
                    self.logger.info(
                        'unknown error with example {0}'
                        .format(common_data['ip_address']))

        self.logger.info('Chunk {0} processed'.format(self.file))

        # clean
        datafile.close()
        os.remove(self.file)

    def process_example(self, example):
        try:
            for interval in self.project.interval:
                current = copy.copy(example)
                current.reduce_interval(interval)
                key, meta = self.session.exists(current)

                if meta is None:
                    self.session.add(current)
                else:
                    db_example = self.session.query(Example).get(current.__key__)
                    current = current + db_example
                    self.session.add(current)
        except Exception as e:
            self.logger.error(
                "Exception in process_record {0}"
                .format(e))

    # def _after(self, *args, **kwargs):
        # time_spent = time.time() - self.init_t

        # Event(
        #     user=self.project.user,
        #     project=self.project.name,
        #     event_type='task',
        #     title='process_data {0} finished in {1:.3f}s'.format(self.file, time_spent),
        #     description='Filename {0}, interval {1}'.format(self.file, self.interval)
        # ).save()
