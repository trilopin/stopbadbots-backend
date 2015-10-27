import falcon
import uuid
import logging
from view import BaseResource
from tasks import chunk
from model.project import Project
import traceback


CHUNK_SIZE = 10000


class Collection(BaseResource):

    def __init__(self, settings):
        super(Collection, self).__init__(settings)
        self.logger = logging.getLogger('example.Collection')

    def on_post(self, req, res, project_name):
        '''Adds new examples by project'''
        try:

            if 'application/octet-stream' not in req.content_type:
                raise falcon.HTTPUnsupportedMediaType(
                    'Must be application/octet-stream content/type')

            # get params
            compress = req.params['compression'] \
                if 'compression' in req.params else None
            interval = req.params['interval'] \
                if 'interval' in req.params else 30
            project_name = "{0}/{1}".format(req.context['user'].user, project_name)
            project = self.session.query(Project).filter_by(full_name=project_name).first()
            self.info('Project get {0}'.format(project.name))

            # write into random filename and call async task for chunking
            filename = self.settings['data_dir'] + str(uuid.uuid4())
            with open(filename, 'wb') as f:
                f.write(req.stream.read())
            self.info('File uploaded to {0}'.format(filename))
            chunk.delay(
                file=filename,
                compress=compress,
                interval=interval,
                project=project)
            self.info('Celery task example_chunk_data created')

            req.context['result'] = ''
            res.status = falcon.HTTP_200
        except Exception as error:
            req.context['result'] = str(error)
            self.error(traceback.format_exc())
            self.error(
                'Exeption caught in example.Collection.post {0}'
                .format(type(error)))
            res.status = falcon.HTTP_500
