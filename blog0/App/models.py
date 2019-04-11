from django.conf import settings
from django.db import models

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="posts")
    title = models.CharField(max_length=120,unique=True)
    body = models.CharField(max_length=200)
    createTimeStamp = models.DateTimeField(auto_now_add=True)
    updateTimeStamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

