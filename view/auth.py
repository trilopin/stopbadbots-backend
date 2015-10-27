import falcon
from model.user import User, Auth
from view import BaseResource

AUTHTOKEN_TTL = 86400


class Authentication(BaseResource):

    def on_options(self, req, res):
        res.set_header('Allow', 'OPTIONS, POST')

    def on_post(self, req, res):
        user = None
        try:
            if 'private_token' in req.context['doc']:
                user = self.session.query(User) \
                    .filter_by(private_token=req.context['doc']['private_token']) \
                    .first()
            elif 'name' in req.context['doc']:
                user = self.session.query(User) \
                    .filter_by(name=req.context['doc']['name']) \
                    .first()
                if 'password' not in req.context['doc']:
                    raise falcon.HTTPBadRequest('Password missing in user/password login', '')
                elif user.password != user.make_password(req.context['doc']['password']):
                    raise falcon.HTTPForbidden('Invalid credentials  in user/password login', '')
            else:
                raise falcon.HTTPBadRequest('Invalid auth request. No user/password neither token passed', '')
        except Exception:
            raise falcon.HTTPForbidden('Invalid credentials in auth request', '')

        auth = Auth({'user': user.name})
        self.session.add(auth, {'ttl': AUTHTOKEN_TTL})

        res.status = falcon.HTTP_200
        req.context['result'] = {'auth_token': str(auth.token)}
