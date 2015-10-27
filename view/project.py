import falcon
from view import BaseResource
from model.project import Project


class Collection(BaseResource):
    def on_options(self, req, res):
        res.set_header('Allow', 'OPTIONS, GET')

    def on_get(self, req, res):

        try:
            projects = self.session.query(Project).filter_by(user=req.context['user'].user)
            projects = [(project.to_primitive()) for project in projects if self._match_host(req.params,project)]
            req.context['result'] = projects
            if len(projects):
                res.status = falcon.HTTP_200
            else:
                res.status = falcon.HTTP_404
        except Exception as e:
            res.status = falcon.HTTP_500
            req.context['result'] = str(e)


    def _match_host(self, params, project):
        if 'host' in params:
            return params['host'] in project.hosts
        else:
            return True

    # def on_post(self, req, res):
    #     '''Creates new project'''

    #     try:

    #         post = req.context['doc']

    #         # cassandra friendly
    #         post['name'] = post['name'].replace('-', '_')

    #         # create model
    #         project = req.context['user'].new_project(**post)
    #         project.save()

    #         req.context['result'] = project.to_dict()
    #         res.status = falcon.HTTP_200
    #     except Exception as e:
    #         req.context['result'] = str(e)
    #         res.status = falcon.HTTP_500


class Item(BaseResource):
    def on_options(self, req, res):
        res.set_header('Allow', 'OPTIONS, GET')

    def on_get(self, req, res, project_name):
        try:
            full_name = "{0}/{1}".format(req.context['user'].user, project_name)
            projects = self.session.query(Project).filter_by(full_name=full_name)
            projects = [(project.to_primitive()) for project in projects]
            res.status = falcon.HTTP_200
            if len(projects) == 1:
                res.status = falcon.HTTP_200
                req.context['result'] = projects[0]
            elif len(projects) > 1:
                res.status = falcon.HTTP_500
            else:
                res.status = falcon.HTTP_404
        except Exception as e:
            res.status = falcon.HTTP_500
            req.context['result'] = str(e)

