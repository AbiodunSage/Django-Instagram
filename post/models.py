from django.contrib.auth.models import User
from django.db import models

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='posts')
    caption = models.CharField(max_length=140, blank=True)

    def __str__(self):
        return self.caption

class PostFile(models.Model):
    file = models.FileField(upload_to='posts/')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_files')

    def __str__(self):
        return self.file.name