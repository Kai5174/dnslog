from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class IscanUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    avatar = models.ImageField(upload_to='avatars/')
    introduction = models.TextField()
    role = models.CharField(max_length=10, default='admin')

    def __str__(self):
        return self.user.username