from mongoauth import authenticate, login, logout

from django.contrib.auth.hashers import make_password, check_password
from django.utils.crypto import get_random_string

from utils.email_templates import (
    ForgotPasswordTemplate,
    PasswordChangedTemplate,
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from mongoauth.api_authentications import (
    SessionAuthenticationUnsafeMethods,
    SessionAuthenticationAllMethods,
    CsrfExemptSessionAuthentication,
)

from mongoauth.mongomodels import User

from utils.email_tasks import send_async_system_email


class LoginAPIView(APIView):
    """A Login API which logs a user in."""
    authentication_classes = (CsrfExemptSessionAuthentication, )

    def post(self, request, format=None):
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return Response({
                'success': True,
                'userId': str(user.id),
                'userEmail': user.email,
                'firstName': user.first_name,
                'lastName': user.last_name}, status=status.HTTP_200_OK)
        else:
            return Response(
                {'success': False, 'message': 'Incorrect email or password'},
                status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({'success': False, 'message': 'Incomplete data'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class LogoutAPIView(APIView):
    """Logs a user out and destroys the user's sesssion"""
    authentication_classes = (SessionAuthenticationAllMethods, )

    def get(self, request):
        logout(request)
        return Response({'success': True, 'message': 'User logged out'}, status=status.HTTP_200_OK)


class TestAPI(APIView):
    authentication_classes = (SessionAuthenticationUnsafeMethods, )
    # permission_classes = (IsSelfOrAdminOrReadOnly, )

    def get_object(self):
        user = User.objects.get(email='testemail@gmail.com')
        self.check_object_permissions(self.request, user.id)
        return user

    def post(self, request):
        # self.get_object()
        key1 = request.data.get('key1')
        key2 = request.data.get('key2')
        send_async_system_email.delay(
            subject='Test Email',
            body='This is a test email!!!',
            email_from='info@gmail.com',
            email_to=['recipient@gmail.com'],
            fail_silently=False)
        return Response({'Yup its working! Values sent %s, %s' % (key1, key2)})


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
                    email_obj = PasswordChangedTemplate()
                    email_obj.recipient_list = [request.user.email]
                    send_async_system_email.delay(
                        email_obj=email_obj,
                        fail_silently=False)
                    return Response(
                        {'success': True, 'message': 'Password has been changed for %s' % request.user.email},
                        status=status.HTTP_200_OK)
                else:
                    return Response(
                        {'success': False, 'message': 'Incorrect user or password'},
                        status=status.HTTP_406_NOT_ACCEPTABLE)
            except User.DoesNotExist:
                return Response(
                    {'success': False, 'message': 'User does not exist'},
                    status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(
                {'success': False, 'message': 'Old password or new password cannot be left blank'},
                status=status.HTTP_406_NOT_ACCEPTABLE)


class ResetPasswordAPIView(APIView):
    """
    Resets a user's password based on the Email Id provided in the query string.
    Also used iin Forgot Password for a User.
    """

    def get(self, request):
        email = request.GET.get('email', None)
        if email:
            try:
                new_password = get_random_string(length=8)
                user = User.objects.get(email=email)
                user.password = make_password(new_password)
                user.save()
                email_obj = ForgotPasswordTemplate()
                email_obj.message = email_obj.message % new_password
                email_obj.context = {'new_password': new_password}
                email_obj.recipient_list = [user.email]
                send_async_system_email.delay(
                    email_obj=email_obj,
                    fail_silently=False)
                return Response(
                    {'success': True, 'message': 'Password has been reset for %s' % email},
                    status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response(
                    {'success': False, 'message': 'Invalid email id'},
                    status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(
                {'success': False, 'message': 'Email cannot be left blank'},
                status=status.HTTP_406_NOT_ACCEPTABLE)
