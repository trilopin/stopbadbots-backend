import bz2
import os
import time
from itertools import islice
from celery import group, chord
from tasks.generictask import GenericTask


class Chunk(GenericTask):

    CHUNK_SIZE = 50000

    allowed_kwargs = [
        'file',
        'compress',
        'interval',
        'project',
        'logger',
        'process_file',
        'simple_stats',
    ]

    def _before(self, *args, **kwargs):
        self.init_t = time.time()

    def _get_file(self):
        if 'bz2' == self.compress:
            return bz2.BZ2File(self.file)
        elif self.compress is None:
            return open(self.file, 'rb')

    def execute(self, *args, **kwargs):
        ''' Chunks filename keeping header and calls next async
            process data action
        '''
        data_in = self._get_file()

        headers = list(islice(data_in, 1))
        part = 1
        tasks = []
        while True:
            line_iter = islice(data_in, self.CHUNK_SIZE)

            try:
                first_line = next(line_iter)
            except StopIteration:
                break

            filename_part = '{0}-part{1:03d}'.format(self.file, part)
            with open(filename_part, 'wb') as fout:
                for line in headers:
                    fout.write(line)
                fout.write(first_line)
                for line in line_iter:
                    fout.write(line)
            part += 1

            tasks.append(
                self.process_file.s(
                    file=filename_part,
                    interval=self.interval,
                    project=self.project)
            )

        # when all process data are done -> outlier detection
        self.logger.info('File chunk {0} completed'.format(self.file))
        self._chain_tasks(tasks)

        data_in.close()
        os.remove(self.file)

    def _chain_tasks(self, tasks):
        process_file = group(*tasks)
        chord(process_file)(self.simple_stats.s(
            project=self.project,
            interval=self.interval)
        )

    # def _after(self, *args, **kwargs):
    #     time_spent = time.time() - self.init_t

    #     Event(
    #         user=self.project.user,
    #         project=self.project.name,
    #         event_type='task',
    #         title='example_chunk_data finished in {0:.3f}s'.format(time_spent),
    #         description='Filename {0}, interval {1}'.format(self.file, self.interval)
    #     ).save()
