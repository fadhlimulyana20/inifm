from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views import View
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

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

class About(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['route'] = 'about'
        return context

class LoginPage(View):
    template_name = "registration/login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('main:home'))
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(username, password)
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return HttpResponseRedirect(request.POST.get('next'))
            return HttpResponseRedirect(reverse('main:home'))
        else:
            messages.error(request, 'Username atau Password Salah')
            return HttpResponseRedirect(reverse('main:login'))