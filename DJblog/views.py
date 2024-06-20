from django.shortcuts import render, redirect
from .models import Post , Comment
from .forms import PostForm

# Create your views here.

def post_list(request):
    posts = Post.objects.all()
    return render(request,'post_list.html',{'posts':posts})

def post_detail(request,post_id):
    post = Post.objects.get(id=post_id)
    return render(request,'post_detail.html',{'post':post})