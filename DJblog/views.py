from django.shortcuts import render, redirect
from .models import Post , Comment
from .forms import PostForm , CommentForm
from django.views.generic import ListView 

# Create your views here.

# def post_list(request):
#     posts = Post.objects.all()
#     return render(request,'post_list.html',{'posts':posts})

class PostList(ListView):
    model = Post
    template_name = "post_list.html"


def post_detail(request,post_id):
    post = Post.objects.get(id=post_id)
    post_comments = Comment.objects.filter(post=post)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.comment_writer = request.user
            myform.post = post
            myform = form.save()
            form = CommentForm()
    else:
        form = CommentForm()
    return render(request,'post_detail.html',{'post':post,'post_comments':post_comments,'form':form})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.writer = request.user
            myform = form.save()
            form = PostForm()
    else:
        form = PostForm()
        
    return render(request,'post_new.html',{'form':form})


def post_edit(request,post_id):
    data = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES,instance=data)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.writer = request.user
            myform = form.save()
            form = PostForm()
    else:
        form = PostForm(instance=data)
    return render(request,'post_edit.html',{'form':form})


def post_delete(request,post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('/DJblog/')