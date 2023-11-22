from django.urls import path,include
from . import views
from rest_framework import routers
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

router = routers.DefaultRouter()
router.register('Post', views.IntruderImage)

urlpatterns = [
path('', views.initial, name='initial'),
path('post/<int:pk>/', views.post_detail, name='post_detail'),
path('post_list', views.post_list, name='post_list'),
path('api_root/', include(router.urls)),
path('register/', views.register_user, name='register_user'),
path('get_global_count/', views.get_global_count, name='get_global_count'),
path('get_today_count/', views.get_today_count, name='get_today_count'),
path('mobile_register/',views.mobile_register_user, name='mobile_register_user'),
path('mobile_login/',views.mobile_login, name='mobile_login'),
path('login/', LoginView.as_view(), name='login'),
 path('logout/', LogoutView.as_view(), name='logout'),
]