from django.shortcuts import render, redirect
from .models import Post , Comment , Profile
from .forms import PostForm , CommentForm , UserRegistrationForm , LoginForm
from django.views.generic import ListView 
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return redirect('/DJblog/login/')  # Replace 'login' with the name of your login URL
    else:
        form = UserRegistrationForm()
    return render(request, 'DJblog/register.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/DJblog/')  # Replace 'home' with the name of your home URL
                else:
                    return render(request, 'DJblog/login.html', {'form': form, 'error': 'Disabled account'})
            else:
                return render(request, 'DJblog/login.html', {'form': form, 'error': 'Invalid login'})
    else:
        form = LoginForm()
    return render(request, 'DJblog/login.html', {'form': form})


# Create your views here.

def post_list(request):
    posts = Post.objects.all()
    return render(request,'DJblog/post_list.html',{'posts':posts})


# class PostList(ListView):
#     model = Post
#     template_name = "post_list.html"


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
    else:
        form = CommentForm()
    return render(request,'DJblog/post_detail.html',{'post':post,'post_comments':post_comments,'form':form})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.writer = request.user
            myform = form.save()
            return redirect('/DJblog/')
    else:
        form = PostForm()
    return render(request,'DJblog/post_new.html',{'form':form})


def post_edit(request,post_id):
    data = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES,instance=data)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.writer = request.user
            myform = form.save()
            # return redirect('/DJblog/')
    else:
        form = PostForm(instance=data)
    return render(request,'DJblog/post_edit.html',{'form':form})


def post_delete(request,post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('/DJblog/')


def comment_edit(request,comment_id,post_id):
    data = Post.objects.get(id=post_id)
    comment_data = Comment.objects.get(id=comment_id,post=data)
    if request.method == 'POST':
        form = CommentForm(request.POST,request.FILES,instance=comment_data)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.writer = request.user
            myform = form.save()
            form = CommentForm()
            return redirect ('/DJblog/')
    else:
        form = CommentForm(instance=comment_data)
    return render(request,'DJblog/post_detail.html',{'form':form})


def comment_delete(request,post_id,comment_id):
    post = Post.objects.get(id=post_id)
    comment = Comment.objects.get(id=comment_id,post=post)
    comment.delete()
    return redirect('/DJblog/')