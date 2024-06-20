from django import forms
from .models import Post , Comment

class PostForm(forms.ModelForm):
    models = Post
    fields = '__all__'