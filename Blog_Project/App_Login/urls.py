from django.urls import path
from . import views

app_name = "App_Login"

urlpatterns = [
    path('sign_up', views.sign_up, name='sign_up'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('forget_password', views.forget_password, name='forget_password'),
    path('reset_password/<str:token>', views.reset_password, name='reset_password'),
]