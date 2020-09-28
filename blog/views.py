from django.shortcuts import get_object_or_404, get_list_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.views import View
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from .forms import PostForm

# Create your views here.
class PostList(ListView):
    template_name = "home.html"
    paginate_by = 5
    queryset = Post.objects.filter(status=1).order_by('-created_at')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context['route'] = 'blog'
        return context

class PostListByCategory(ListView):
    template_name = "archive.html"
    paginate_by = 5
    # queryset = Post.objects.filter(status=1).order_by('-created_at')

    def get_queryset(self):
        return get_list_or_404(Post.objects.order_by('-created_at'),
            status=1,
            category__slug= self.kwargs['category_slug']
        )

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        archive_name = self.kwargs['category_slug']
        archive_name = archive_name.replace("-", " ")
        context['archive'] = archive_name.title()
        context['route'] = 'blog'
        return context

class PostDetail(DetailView):
    template_name = "post-detail.html"
    model = Post

    def get_object(self, queryset=None):
        return get_object_or_404(Post,
            category__slug=self.kwargs['category_slug'],
            slug=self.kwargs['slug']
        )

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['meta'] = self.get_object().as_meta(self.request)
        print(context['meta'])
        # Add in the publisher
        context['route'] = 'blog'
        return context

class CreatePost(LoginRequiredMixin, FormView):
    template_name = "create-post.html"
    login_url = '/login/'
    form_class = PostForm

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return HttpResponseRedirect(reverse('blog:create_post'))


