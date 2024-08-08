from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from utils.generate_code import generate_code
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=20000)
    writer = models.ForeignKey(User,related_name='post_writer',on_delete=models.SET_NULL,null=True,blank=True)
    drafted = models.BooleanField(default=True)
    tags = TaggableManager()
    created_at = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to="posts_images")

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    comment = models.CharField(max_length=200)
    post = models.ForeignKey(Post,related_name='comment_post',on_delete=models.CASCADE)
    comment_writer = models.ForeignKey(User,related_name='comment_writer',on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.post)
    


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile_user', on_delete=models.CASCADE)
    email = models.EmailField(max_length=254, null=True, blank=True)
    code = models.CharField(max_length=10, default=generate_code)

    def __str__(self):
        return str(self.user)


    @receiver(post_save, sender = User)
    def create_profile(sender, instance, created, **kwargs):
        if created :
            Profile.objects.create (
                user = instance 
            )

