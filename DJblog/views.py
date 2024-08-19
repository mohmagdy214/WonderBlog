from django.shortcuts import render, redirect
from .models import Post , Comment 
from .forms import PostForm , CommentForm , RegisterForm 
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required




def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/DJblog/')
    else:
        form = RegisterForm()
    return render(request, 'registration/sign_up.html', {'form':form})



@login_required(login_url='/login')
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'DJblog/post_list.html', {'posts':posts})



def logout_User(request):
    logout(request)
    return redirect('/login')

# class PostList(ListView):
#     model = Post
#     template_name = "post_list.html"


@login_required(login_url='/login')
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


@login_required(login_url='/login')
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


@login_required(login_url='/login')
def post_edit(request,post_id):
    data = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES,instance=data)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.writer = request.user
            myform = form.save()
            return redirect(f'/DJblog/{post_id}')
    else:
        form = PostForm(instance=data)
    return render(request,'DJblog/post_edit.html',{'form':form})


@login_required(login_url='/login')
def post_delete(request,post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('/DJblog/')


@login_required(login_url='/login')
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
            return redirect(f'/DJblog/{post_id}')
    else:
        form = CommentForm(instance=comment_data)
    return render(request,'DJblog/post_detail.html',{'form':form})


@login_required(login_url='/login')
def comment_delete(request, post_id,comment_id):
    post = Post.objects.get(id=post_id)
    comment = Comment.objects.get(id=comment_id,post=post)
    comment.delete()
    return redirect(f'/DJblog/{post_id}')