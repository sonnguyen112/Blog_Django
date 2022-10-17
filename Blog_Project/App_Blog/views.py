from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth.models import User
from App_Blog.models import Blog, Comment, Like
import os
import uuid
from json import dumps

# Create your views here.
def blogs(request):
    blogs = Blog.objects.all()
    context = {
        'blogs': blogs,
    }
    return render(request, 'App_Blog/blogs.html', context)

@login_required
def profile(request):
    return render(request, 'App_Blog/profile.html')

@login_required
def change_profile(request):
    if request.method == "POST":
        user = request.user
        username = request.POST.get('username')
        email = request.POST.get('email')
        messages = ''
        if User.objects.filter(username=username).exists():
            if username != user.username:
                messages = "Username already exists"
                return render(request, 'App_Blog/change_profile.html', {"message":messages})
        if User.objects.filter(email=email).exists():
            if email != user.email:
                messages = "Email already exists"
                return render(request, 'App_Blog/change_profile.html', {"message":messages})
        user.username = username
        user.email = email
        user.save()
        try:
            if request.FILES["upload"]:
                if settings.USE_S3:
                    img = request.FILES["upload"]
                    user.user_profile.profile_pic = img
                    user.user_profile.save()
                else:
                    img = request.FILES["upload"]
                    fss = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'profile_pics'), base_url=os.path.join(settings.MEDIA_URL, 'profile_pics'))
                    file = fss.save(img.name, img)
                    user.user_profile.profile_pic = fss.url(file).replace("/media/", "")
                    user.user_profile.save()
                return redirect(reverse("App_Blog:profile"))
        except:
            return redirect(reverse("App_Blog:profile"))
    return render(request, 'App_Blog/change_profile.html')

@login_required
def change_password(request):
    if request.method == "POST":
        user = request.user
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        messages = ''
        if user.check_password(old_password):
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages = "Password changed successfully"
                return redirect(reverse("App_Login:login"))
            else:
                messages = "New password and confirm password do not match"
                return render(request, 'App_Blog/change_password.html', {"message":messages})
        else:
            messages = "Old password is incorrect"
            return render(request, 'App_Blog/change_password.html', {"message":messages})
    return render(request, 'App_Blog/change_password.html')

@login_required
def write_blog(request):
    if request.method == "POST":
        title = request.POST.get('title')
        body = request.POST.get('body')
        slug = title.replace(" ", "-") + str(uuid.uuid4())
        user = request.user
        blog_image = request.FILES["blog_image"]
        if settings.USE_S3:
            blog = Blog(title=title, body=body, slug=slug, author=user, blog_image=blog_image)
            blog.save()
        else:
            fss = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'blog_images'), base_url=os.path.join(settings.MEDIA_URL, 'blog_images'))
            file = fss.save(blog_image.name, blog_image)
            blog = Blog(title=title, body=body, author=user, blog_image=fss.url(file).replace("/media/", ""), slug=slug)
            blog.save()
        return redirect(reverse("App_Blog:blogs"))
    return render(request, 'App_Blog/write_blog.html')

@login_required
def blog_detail(request, slug):
    if request.method == "POST":
        comment_content = request.POST.get('comment')
        cur_blog = Blog.objects.get(slug=slug)
        user = request.user
        comment = Comment(body=comment_content, author=user, blog=cur_blog)
        comment.save()
        return redirect(reverse("App_Blog:blog_detail", kwargs={"slug":slug}))
    blog = Blog.objects.get(slug=slug)
    comments = Comment.objects.filter(blog=blog)
    already_liked = Like.objects.filter(blog=blog, author=request.user)
    if already_liked:
        liked = True
    else:
        liked = False
    data_for_js = {
        "slug":slug,
        "liked":liked,
        "url_like":reverse("App_Blog:like_blog", kwargs={"slug":slug}),
        "num_like":blog.blog_like.count(),
        "num_comment":blog.blog_comment.count(),
    }
    data_for_js = dumps(data_for_js)
    context = {
        'blog': blog,
        'comments': comments,
        'data_for_js': data_for_js,
    }
    return render(request, 'App_Blog/blog_detail.html', context)

@login_required
def like_blog(request, slug):
    blog = Blog.objects.get(slug=slug)
    user = request.user
    already_like = Like.objects.filter(author=user, blog=blog)
    if already_like:
        already_like.delete()
    else:
        like = Like(blog=blog, author=user)
        like.save()
    return redirect(reverse("App_Blog:blog_detail", kwargs={"slug":slug}))

@login_required
def my_blogs(request):
    blogs = Blog.objects.filter(author=request.user)
    context = {
        'blogs': blogs,
    }
    return render(request, 'App_Blog/my_blogs.html', context)

@login_required
def update_blog(request, slug):
    blog = Blog.objects.get(slug=slug)
    if request.method == "POST":
        blog.title = request.POST.get('title')
        blog.body = request.POST.get('body')
        blog_image = request.FILES["blog_image"]
        if settings.USE_S3:
            blog.blog_image = blog_image
            blog.save()
        else:
            fss = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'blog_images'), base_url=os.path.join(settings.MEDIA_URL, 'blog_images'))
            file = fss.save(blog_image.name, blog_image)
            blog.blog_image = fss.url(file).replace("/media/", "")
        blog.slug = blog.title.replace(" ", "-") + str(uuid.uuid4())
        blog.save()
        return redirect(reverse("App_Blog:my_blogs"))
    return render(request, 'App_Blog/update_blog.html', {"blog":blog})