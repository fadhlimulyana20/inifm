from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post

# Create your views here.
class PostList(ListView):
    template_name = "home.html"
    queryset = Post.objects.filter(status=1).order_by('-created_at')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context['posts'] = self.queryset
        context['route'] = 'blog'
        return context

class PostDetail(DetailView):
    template_name = "post-detail.html"
    model = Post

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context['route'] = 'blog'
        return context
