from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField()
    code = models.TextField(blank=True)
    code_language = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Community(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
