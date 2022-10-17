from django.urls import path
from . import views

app_name = "App_Blog"

urlpatterns = [
    path('', views.blogs, name='blogs'),
    path('profile', views.profile, name='profile'),
    path('change_profile', views.change_profile, name='change_profile'),
    path('change_password', views.change_password, name='change_password'),
    path('write_blog', views.write_blog, name='write_blog'),
    path('details/<str:slug>', views.blog_detail, name='blog_detail'),
    path('like/<str:slug>', views.like_blog, name='like_blog'),
    path('my_blogs', views.my_blogs, name='my_blogs'),
    path('update_blog/<str:slug>', views.update_blog, name='update_blog'),
]