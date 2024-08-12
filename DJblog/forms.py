from django import forms
from .models import Post , Comment 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2','email']
        


class PostForm(forms.ModelForm):
    class Meta :
        model = Post
        exclude = ('writer',)

class CommentForm(forms.ModelForm):
    class Meta :
        model = Comment
        fields = ['comment']