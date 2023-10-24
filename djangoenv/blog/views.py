from django.shortcuts import render, redirect
from rest_framework import viewsets
from .serializers import PostSerializer
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

def initial(request):
    return render(request,'blog/base.html')

def post_list(request):
    posts = Post.objects.all()  # Assuming you want to fetch all posts
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

class IntruderImage(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

def register_user(request):
    if request.method == 'POST':
        print(request)
        try:
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST["email"]
            
            new_user = User.objects.create_user(username=username, password=password, email=email)
            new_user.save()
            return render(request, 'blog/base.html', {'message': '회원가입이 완료됨'})
        except Exception as e:
            return render(request, 'blog/register.html', {'message': '회원이 이미 있음'})
    else:
        return render(request, 'blog/register.html')
