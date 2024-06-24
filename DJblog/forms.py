from django import forms
from .models import Post , Comment

class PostForm(forms.ModelForm):
    class Meta :
        model = Post
        exclude = ('writer',)

class CommentForm(forms.ModelForm):
    class Meta :
        model = Comment
        fields = ['comment']