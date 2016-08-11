from mongoauth import authenticate, login, logout

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import View


class LoginView(View):
    """
    A login page for testing purposes.
    """

    template_name = 'mongoauth/login.html'

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/auth/login/success/')
        else:
            return HttpResponseRedirect('/auth/login/fail/')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/auth/login/')


class LoginSuccessView(View):
    template_name = 'mongoauth/login_success.html'

    def get(self, request):
        return render(request, self.template_name, {})


class LoginFailView(View):
    template_name = 'mongoauth/login_fail.html'

    def get(self, request):
        return render(request, self.template_name, {})
