from django.urls import path
from . import views
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('', views.getRoutes),
    path('register/', views.registrationView, name='register'),
     path('users/', views.getUsers, name='users'),
    path('user/', views.getUserbyEmail, name='user'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/', views.login, name='login'),
  

   ]