from django.urls import path
from .views import Home, LoginPage, About

app_name = 'main'
urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('tentang', About.as_view(), name='about'),
    path('login/', LoginPage.as_view(), name='login')
]