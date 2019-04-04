from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.

def hello(request):
    context = {
        "name":"Django",
        "version":2.1,
        "users":["ram","jack","tom","dj","qwe"]
    }
    return render(request,"index.html",context=context)

def home(request):
    if request.method == "GET":
        return render(request,"home.html")

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        print(f"my name is {username} and my email is {email} and won't tell my password ")
        return HttpResponse("hey it is post")

def post(request):
    if request.method == "GET":
        posts = Post.objects.all()
        context = {
            'posts':posts
        }
        return render(request, "post.html",context)

    if request.method == "POST":
        title = request.POST["title"]
        body = request.POST["body"]
        print(title,body)
        return HttpResponse("hey it is post")


