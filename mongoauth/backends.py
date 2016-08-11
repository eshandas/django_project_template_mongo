from django.contrib.auth.hashers import check_password
from .mongomodels import User

SESSION_KEY = '_auth_user_id'
BACKEND_SESSION_KEY = '_auth_user_backend'
HASH_SESSION_KEY = '_auth_user_hash'
REDIRECT_FIELD_NAME = 'next'


class MongoAuthBackend(object):
    def authenticate(self, email=None, password=None):
        user = User.objects(email=email)
        # return user

        if user:
            user = user[0]
        else:
            return None

        if check_password(password, user.password):
            # Authentication success by returning the user
            return user
        else:
            # Authentication fails if None is returned
            return None

    def get_user(self, user_id):
        user = User.objects(id=user_id)
        # user.pk = user._id
        # return user

        if user:
            return user[0]
        else:
            return None
