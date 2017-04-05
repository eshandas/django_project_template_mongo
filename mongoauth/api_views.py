from mongoauth import authenticate, login, logout

from django.contrib.auth.hashers import make_password, check_password
from django.utils.crypto import get_random_string

from tasks.email_tasks.emailer import Emailer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from mongoauth.api_authentications import (
    SessionAuthenticationUnsafeMethods,
    SessionAuthenticationAllMethods,
    CsrfExemptSessionAuthentication,
)

from mongoauth.mongomodels import User

from utils.response_handler import generic_response


class LoginAPIView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, )

    def post(self, request, format=None):
        """
        A Login API which logs a user in.
        """
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            return Response({
                'success': True,
                'userId': str(user.id),
                'userEmail': user.email,
                'firstName': user.first_name,
                'lastName': user.last_name}, status=status.HTTP_200_OK)
        else:
            return Response(
                generic_response('Incorrect email or password'),
                status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(
            generic_response('Incomplete data'),
            status=status.HTTP_406_NOT_ACCEPTABLE)


class LogoutAPIView(APIView):
    authentication_classes = (SessionAuthenticationAllMethods, )

    def get(self, request):
        """
        Logs a user out and destroys the user's sesssion
        """
        logout(request)
        return Response(
            generic_response('User logged out'),
            status=status.HTTP_200_OK)


class TestAPI(APIView):
    authentication_classes = (SessionAuthenticationUnsafeMethods, )
    # permission_classes = (IsSelfOrAdminOrReadOnly, )

    def get_object(self):
        user = User.objects.get(email='testemail@gmail.com')
        self.check_object_permissions(self.request, user.id)
        return user

    def post(self, request):
        key1 = request.data.get('key1')
        key2 = request.data.get('key2')
        # Send a test email
        Emailer(
            subject='subject',
            message='message',
            recipient_list=['sendto@somecompany.com'],
            email_template='email_templates/test_template.html',
            context={'foo': 'BATMAN'}).send_email(send_async=False, fail_silently=True)
        return Response(
            generic_response('Yup its working! Values sent %s, %s' % (key1, key2)),
            status=status.HTTP_200_OK)


class ChangePasswordAPIView(APIView):
    """
    Change the account password by providing the current password.
    """
    authentication_classes = (SessionAuthenticationUnsafeMethods, )

    def post(self, request, format=None):
        old_password = request.data.get('old_password', None)
        new_password = request.data.get('new_password', None)
        if old_password and new_password:
            try:
                if check_password(old_password, request.user.password):
                    request.user.password = make_password(new_password)
                    request.user.save()
                    # Send an email
                    Emailer(
                        subject='Password changed',
                        message='Your password was changed successfully',
                        recipient_list=[request.user.email],
                        email_template='mongoauth/emails/change_password.html',
                        context={}).send_email(send_async=False, fail_silently=True)
                    return Response(
                        generic_response('Password has been changed for %s' % request.user.email),
                        status=status.HTTP_200_OK)
                else:
                    return Response(
                        {'success': False, 'message': 'Incorrect user or password'},
                        status=status.HTTP_406_NOT_ACCEPTABLE)
            except User.DoesNotExist:
                return Response(
                    generic_response('User does not exist'),
                    status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(
                generic_response('Old password or new password cannot be left blank'),
                status=status.HTTP_406_NOT_ACCEPTABLE)


class ResetPasswordAPIView(APIView):

    def get(self, request):
        """
        Resets a user's password based on the Email Id provided in the query string.
        Also used iin Forgot Password for a User.
        """
        email = request.GET.get('email', None)
        if email:
            try:
                new_password = get_random_string(length=8)
                user = User.objects.get(email=email)
                user.password = make_password(new_password)
                user.save()
                # Send email
                Emailer(
                    subject='Request for password reset',
                    message='Your new password is %s' % new_password,
                    recipient_list=[user.email],
                    email_template='mongoauth/emails/reset_password.html',
                    context={'new_password': new_password}).send_email(send_async=False, fail_silently=True)
                return Response(
                    generic_response('Password has been reset for %s' % email),
                    status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response(
                    generic_response('Invalid email id'),
                    status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(
                generic_response('Email cannot be left blank'),
                status=status.HTTP_406_NOT_ACCEPTABLE)
