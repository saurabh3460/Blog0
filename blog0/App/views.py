from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponse,HttpResponseRedirect
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
        context = {'posts':posts
}
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


# a help full link for update data
# https://stackoverflow.com/questions/49245098/how-can-i-update-data-in-django-orm-or-django-shell
