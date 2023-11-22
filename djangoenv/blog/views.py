from django.shortcuts import render, redirect
from rest_framework import viewsets
from .serializers import PostSerializer
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import SignUpSerializer
from .models import GlobalPostCount,ResponseModel
from django.contrib.auth import authenticate, login
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from datetime import date
from django.db.models import Sum

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
    

def get_global_count(request):
    # GlobalPostCount 모델의 count 반환
    global_count = GlobalPostCount.objects.first()
    return JsonResponse({'global_count': global_count})

def get_today_count(request):
    # 오늘의 count 반환
    today_count = Post.objects.filter(created_date__date=date.today()).aggregate(Sum('count'))['count__sum']
    return JsonResponse({'today_count': today_count})

@api_view(['POST'])
def mobile_register_user(request):
    if request.method == 'POST':
        serializer = SignUpSerializer(data=request.data)
        response_data = None
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            email = serializer.validated_data['email']

            # Check if the user already exists
            if User.objects.filter(username=username).exists():
                response_data = ResponseModel(issuccess=False, message="이미 가입된 사용자가 있습니다.")
                return Response({'status': response_data.status,
                'message': response_data.message,
                'issuccess': response_data.issuccess,}, status=status.HTTP_400_BAD_REQUEST)

            # Create a new user
            new_user = User.objects.create_user(username=username, password=password, email=email)
            new_user.save()

            response_data = ResponseModel(issuccess=True, message="회원가입이 완료되었습니다.")
            return Response({'status': response_data.status,
                'message': response_data.message,
                'issuccess': response_data.issuccess,},status=status.HTTP_201_CREATED)

        return Response({'status': response_data.status,
                'message': response_data.message,
                'issuccess': response_data.issuccess,}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def mobile_login(request):
    if request.method == 'POST':
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        # Check if the provided credentials are valid
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            response_data = {
                'status': 'success',
                'message': 'Login successful',
                'issuccess': True,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        else:
            response_data = {
                'status': 'error',
                'message': 'Invalid credentials',
                'issuccess': False,
            }

            return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)

