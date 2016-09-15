from django.shortcuts import render
from django.views.generic import View

from .mongomodels import Post


class PostsView(View):
    template_name = 'posts/all_posts.html'

    def get(self, request):
        posts = Post.objects.all()
        context = {'posts': posts}
        return render(request, self.template_name, context)
