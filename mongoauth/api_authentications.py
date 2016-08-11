from django.contrib.sessions.backends.db import SessionStore

from errorlog.middleware.errormiddleware import log_session_error

from .mongomodels import User
from django.contrib.auth.models import AnonymousUser

from rest_framework import authentication
from rest_framework import exceptions
from rest_framework.permissions import SAFE_METHODS


def getSessionId(request):
    session_id = request.COOKIES.get('sessionid', '')
    if not session_id:
        session_id = request.META.get('HTTP_SESSIONID', '')
        if not session_id:
            request.user = AnonymousUser()
            log_session_error(request, exceptions.AuthenticationFailed('Session id token not found'))
            raise exceptions.AuthenticationFailed('Session id token not found')
    return session_id


class SessionAuthenticationUnsafeMethods(authentication.BaseAuthentication):
    """
    Session Id is expected only for UNSAFE methods, i.e: PUT, POST, DELETE
    SAFE_METHODS get free passage and Session Id is not checked.
    Session Id can be passed in Cookie or Request Header with key: sessionid
    """
    def authenticate(self, request):
        if request.method in SAFE_METHODS:
            return (None, None)

        session_id = getSessionId(request)
        sessionStore = SessionStore(session_key=session_id)
        uid = sessionStore.get('_auth_user_id', '')

        # Add the session object into request
        request.session = sessionStore

        if not uid:
            request.user = AnonymousUser()
            log_session_error(request, exceptions.AuthenticationFailed('Invalid session id token: %s' % session_id))
            raise exceptions.AuthenticationFailed('Invalid session id token: %s' % session_id)
        try:
            user = User.objects.get(id=uid)
        except User.DoesNotExist:
            request.user = AnonymousUser()
            log_session_error(request, exceptions.AuthenticationFailed('User does not exist for this session token %s' % session_id))
            raise exceptions.AuthenticationFailed('User does not exist for this session token %s' % session_id)

        return (user, None)


class SessionAuthenticationAllMethods(authentication.BaseAuthentication):
    """
    A Session Id is expected for any kind of request.
    If a valid Session Id is not present, error will be raised.
    Session Id can be passed in Cookie or Request Header with key: sessionid
    """
    def authenticate(self, request):
        session_id = getSessionId(request)
        sessionStore = SessionStore(session_key=session_id)
        uid = sessionStore.get('_auth_user_id', '')

        # Add the session object into request
        request.session = sessionStore

        if not uid:
            request.user = AnonymousUser()
            log_session_error(request, exceptions.AuthenticationFailed('Invalid session id token: %s' % session_id))
            raise exceptions.AuthenticationFailed('Invalid session id token: %s' % session_id)
        try:
            user = User.objects.get(id=uid)
        except User.DoesNotExist:
            request.user = AnonymousUser()
            log_session_error(request, exceptions.AuthenticationFailed('User does not exist for this session token %s' % session_id))
            raise exceptions.AuthenticationFailed('User does not exist for this session token %s' % session_id)

        return (user, None)


class CsrfExemptSessionAuthentication(authentication.BaseAuthentication):
    """
    Use Django's session framework for authentication. But bypass the CSRF token check mechanism.
    """

    def authenticate(self, request):
        """
        Returns a `User` if the request session currently has a logged in user.
        Otherwise returns `None`.
        """
        # Get the session-based user from the underlying HttpRequest object
        user = getattr(request._request, 'user', None)

        # Unauthenticated, CSRF validation not required
        if not user or not user.is_active:
            return None

        # If authenticated user
        return (user, None)
