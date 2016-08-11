from django.conf.urls import url

from .views import (
    LoginView,
    LoginSuccessView,
    LoginFailView,
    LogoutView,
)

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^login/success/$', LoginSuccessView.as_view(), name='login_success'),
    url(r'^login/fail/$', LoginFailView.as_view(), name='login_fail'),
]
