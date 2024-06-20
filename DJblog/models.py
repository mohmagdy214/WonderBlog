from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=20000)
    writer = models.ForeignKey(User,related_name='post_writer',on_delete=models.SET_NULL,null=True,blank=True)
    drafted = models.BooleanField(default=True)
    tags = TaggableManager()
    created_at = models.DateTimeField(default=timezone.now())
    image = models.ImageField(upload_to="posts_images")

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    comment = models.CharField(max_length=200)
    post = models.ForeignKey(Post,related_name='comment_post',on_delete=models.CASCADE)
    writer = models.ForeignKey(User,related_name='comment_writer',on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.comment