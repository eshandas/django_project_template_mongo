import mongoauth
from django.utils.functional import SimpleLazyObject


def get_user(request):
    if not hasattr(request, '_cached_user'):
        request._cached_user = mongoauth.get_user(request)
    return request._cached_user


class AuthenticationMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'session'), (
            "The Django authentication middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE_CLASSES setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "'django.contrib.auth.middleware.AuthenticationMiddleware'."
        )
        request.user = SimpleLazyObject(lambda: get_user(request))


class SessionAuthenticationMiddleware(object):
    """
    Formerly, a middleware for invalidating a user's sessions that don't
    correspond to the user's current session authentication hash. However, it
    caused the "Vary: Cookie" header on all responses.

    Now a backwards compatibility shim that enables session verification in
    auth.get_user() if this middleware is in MIDDLEWARE_CLASSES.
    """
    def process_request(self, request):
        pass


class SessionMiddleware(object):
    def process_response(self, request, response):
        """
        If request.session was modified, or if the configuration is to save the
        session every time, save the changes and set a session cookie or delete
        the session cookie if the session has been emptied.
        """
        try:
            csrftoken = response.cookies.get('csrftoken').value
            response['csrftoken'] = csrftoken
            sessionid = response.cookies.get('sessionid').value
            response['sessionid'] = sessionid
        except:
            pass
        # import ipdb; ipdb.set_trace()
        return response
