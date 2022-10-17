from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    profile_pic = models.FileField(upload_to='profile_pics', blank=True)
    token_for_reset_password = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username
