from django.urls import path
from .views import PostList, PostDetail, CreatePost, PostListByCategory

app_name = "blog"
urlpatterns = [
    path('', PostList.as_view()),
    path('create/', CreatePost.as_view(), name='create_post'),
    path('<slug:category_slug>/', PostListByCategory.as_view(), name='post_list_by_category'),
    path('<slug:category_slug>/<slug:slug>/', PostDetail.as_view(), name='post_detail'),
]
