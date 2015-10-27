import falcon
from view import BaseResource
from model.user import User
import traceback


class Collection(BaseResource):

    def on_get(self, req, res):

        users = [user.to_dict() for user in User.objects.all()]

        res.status = falcon.HTTP_200
        req.context['result'] = users

    def on_post(self, req, res):

        user = User.if_not_exists().create(**req.context['doc'])
        if 'password' in req.context['doc']:
            user.password = user.make_password(req.context['doc']['password'])
        user.save()

        res.status = falcon.HTTP_200
        req.context['result'] = user.to_dict()


class Item(BaseResource):

    def on_get(self, req, res, user):

        try:
            user = self.session.query(User).filter_by(name=user).first()

            res.status = falcon.HTTP_200
            req.context['result'] = user.to_primitive()
        except Exception:
            print(traceback.format_exc())
            res.status = falcon.HTTP_404

    def on_put(self, req, res, user):

        try:
            user = User.get(name=user)

            # prevent update by partition key
            if 'name' in req.context['doc']:
                res.status = falcon.HTTP_400
                req.context['result'] = 'Can\'t update user name'

            # make password
            if 'password' in req.context['doc']:
                req.context['doc']['password'] = user.make_password(
                    req.context['doc']['password'])

            user = user.update(**req.context['doc'])

            res.status = falcon.HTTP_200
            req.context['result'] = user.to_primitive()
        except DoesNotExist:
            res.status = falcon.HTTP_404
