from django.conf.urls import url

from .api_views import (
    LoginAPIView,
    LogoutAPIView,
    ResetPasswordAPIView,
    ChangePasswordAPIView,
    TestAPI,
)

urlpatterns = [
    url(r'^login/$', LoginAPIView.as_view(), name='login'),
    url(r'^logout/$', LogoutAPIView.as_view(), name='logout'),
    url(r'^password/reset/$', ResetPasswordAPIView.as_view(), name='reset_password'),
    url(r'^password/change/$', ChangePasswordAPIView.as_view(), name='change_password'),
    url(r'^test/$', TestAPI.as_view(), name='test'),
]
