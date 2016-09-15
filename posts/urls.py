from django.conf.urls import url

from .views import (
    PostsView,
)

urlpatterns = [
    url(r'^all/$', PostsView.as_view(), name='all_posts'),
]
