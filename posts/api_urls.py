from django.conf.urls import url

from .api_views import (
    PostAPI,
    PostsAPI,
)

urlpatterns = [
    url(r'^$', PostsAPI.as_view(), name='posts'),
    url(r'^(?P<post_id>[a-zA-Z0-9]+)/$', PostAPI.as_view(), name='post'),
]
