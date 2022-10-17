from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    pulish_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_author")
    update_date = models.DateTimeField(auto_now=True)
    blog_image = models.FileField(upload_to='blog_images', blank=True)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ["-update_date"]

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="blog_comment")
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_author")
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.body

    class Meta:
        ordering = ["-create_date"]

class Like(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="blog_like")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_like")
    def __str__(self):
        return self.author.username