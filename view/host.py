import falcon
from view import BaseResource
from model.host import Host



class Collection(BaseResource):


    def on_get(self, req, res):

        try:
            user_name = req.context['user'].name
            q = Host.objects(user=user_name) #.allow_filtering()
            hosts = [(host.to_dict()) for host in q.all()]

            res.status = falcon.HTTP_200
            req.context['result'] = hosts
        except Exception:
            res.status = falcon.HTTP_404

