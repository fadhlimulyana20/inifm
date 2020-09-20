from django.shortcuts import render
from django.views.generic.base import TemplateView

from blog.models import Post

# Create your views here.
class Home(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(status=1).order_by('-created_at')[:4]
        context['route'] = 'home'
        return context


