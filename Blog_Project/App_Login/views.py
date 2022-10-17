from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .helpers import send_forget_password_mail
import uuid
# Create your views here. 
def sign_up(request):
    messages = {
            "status":'',
            "message":'',
        }
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('password_confirm')
        email = request.POST.get('email')
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages["status"] = "error"
                messages["message"] = "Username already exists"
            elif User.objects.filter(email=email).exists():
                messages["status"] = "error"
                messages["message"] = "Email already exists"
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                user_profile = UserProfile.objects.create(user=user, profile_pic="default.png")
                user_profile.save()
                messages["status"] = "success"
                messages["message"] = "User created successfully"
                return redirect(reverse("App_Login:login") + "?message=User created successfully")
        else:
            messages["status"] = "error"
            messages["message"] = "Password and confirm password do not match"
    return render(request, 'App_Login/sign_up.html', messages)

def login_user(request):
    messages = request.GET.get('message')
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(reverse("App_Blog:blogs"))
        else:
            messages = "Invalid username or password"
    return render(request, 'App_Login/login.html', {"message":messages})

@login_required
def logout_user(request):
    logout(request)
    return redirect(reverse("App_Login:login"))

def forget_password(request):
    message = ''
    if request.method == "POST":
        email = request.POST.get("email")
        if User.objects.filter(email=email).exists():
            token = str(uuid.uuid4())
            user = User.objects.get(email=email)
            user.user_profile.token_for_reset_password = token
            user.user_profile.save()
            send_forget_password_mail(email, token)
            message = "Email already sent"
        else:
            message = "Email does not exists"
    return render(request, 'App_Login/forget_password.html', {"message":message})

def reset_password(request, token):
    message = ''
    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm-password")
        if password == confirm_password:
            profile_obj = UserProfile.objects.get(token_for_reset_password=token)
            user = profile_obj.user
            user.set_password(password)
            user.save()
            message = "Password changed successfully"
            return redirect(reverse("App_Login:login") + "?message=" + message)
        else:
            message = "Password and confirm password do not match"
    return render(request, 'App_Login/reset_password.html', {"message":message})