from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post

# Create your views here.
class PostList(ListView):
    template_name = "home.html"
    queryset = Post.objects.filter(status=1).order_by('-created_at')

class PostDetail(DetailView):
    template_name = "post-detail.html"
    model = Post
