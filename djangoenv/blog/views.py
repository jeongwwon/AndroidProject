from django.shortcuts import render
from rest_framework import viewsets
from .serializers import PostSerializer
from django.shortcuts import render, get_object_or_404
from .models import Post

def post_list(request):
    posts = Post.objects.all()  # Assuming you want to fetch all posts
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

class IntruderImage(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer