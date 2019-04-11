from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import get_user_model, login as user_login, logout, authenticate
User = get_user_model()

from django.urls import reverse
from .models import *

# Create your views here.

def hello(request):
    posts = Post.objects.all()
    context = { 'posts': posts }
    return render(request,"index.html",context=context)

def post(request):
    if request.method == "GET":
        posts = Post.objects.all()
        context = {'posts':posts}
        return render(request, "post.html",context)

    if request.method == "POST":
        title = request.POST["title"]
        body = request.POST["body"]
        post = { "title":title, "body":body }
        try:
            result = Post(**post)
            if result:
                result.save()
                return HttpResponseRedirect("/post")
        except IntegrityError:
            return HttpResponse("Please enter unique title")
        else:
            return HttpResponse("Please enter valid Data")

def deletePost(request,postId):
    print(postId)
    try:
        result = Post.objects.get(id=postId)
        print(result)
        result.delete()
        return HttpResponseRedirect("/post")
    except Post.DoesNotExist:
        return HttpResponse("No Data")

def singlePost(request,postId):

    if request.method == "GET":
        post = Post.objects.get(id=postId)
        return render(request,"singlePost.html",{"post":post})

    if request.method == "POST":
        title = request.POST["title"]
        body = request.POST["body"]
        post = Post.objects.get(id=postId)
        if post:
            post.title = title
            post.body = body
            post.save()
            return HttpResponseRedirect("/post")
        else:
            return HttpResponse("something went wrong")

def signup(request):
    if not request.user.is_authenticated:
        if request.method == "GET":
            return render(request, 'signup.html')

        if request.method == "POST":
            context = {
                "username": request.POST["username"],
                "email": request.POST["email"],
                "password": request.POST["password"],
            }
            try:
                user = User.objects.create_user(**context)
                user.is_active = True
                user_login(request, user)
                print(context)
                return HttpResponseRedirect(reverse('post'))
            except IntegrityError:
                return HttpResponse({"status": 400, "msg": "username or email already exits"})
    else: return HttpResponseRedirect(reverse('post'))


def login(request):
    if not request.user.is_authenticated:
        if request.method == "GET":
            return render(request, "login.html")

        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            print(username, password)
            user = authenticate(username=username, password=password)
            if user is not None:
                user_login(request, user)
                return HttpResponseRedirect(reverse('post'))
            else:
                return HttpResponse("please Enter valid User Data")
    else:
        return HttpResponseRedirect(reverse('post'))

def userPost(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            user = User.objects.get(username=request.user)
            posts = user.posts.all
            context = {'posts': posts}
            return render(request, "post.html", context)

        if request.method == "POST":
            title = request.POST["title"]
            body = request.POST["body"]
            post = {"author":request.user, "title": title, "body": body}
            try:
                result = Post(**post)
                if result:
                    result.save()
                    return HttpResponseRedirect("/userpost")
            except IntegrityError:
                return HttpResponse("Please enter unique title")

    else:
        return HttpResponseRedirect(reverse('login'))



@login_required
def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))




# a help full link for update data
# https://stackoverflow.com/questions/49245098/how-can-i-update-data-in-django-orm-or-django-shell
