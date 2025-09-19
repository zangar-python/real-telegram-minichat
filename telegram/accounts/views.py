from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .user_serializer import UserSerializer
from rest_framework.request import Request
from rest_framework.permissions import AllowAny

from .user_class import UserFunctions

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self,request:Request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        if not username or not password:
            return Response({"error":"Напишите имя и пароль для пользователья!"},status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({"error":"Пользователь с таким именем уже существует!"},status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username,password=password,email=email)
        token , _ = Token.objects.get_or_create(user=user)
        
        user_function = UserFunctions(user=user)
        if not user_function.user_register_to_redis():
            user.delete()
            return Response({"error":"Errrrror"})
        return Response(
            data={
                "from":"Register view",
                "data":user_function.detail(token_key=token.key)
            }
        )

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self,request:Request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response({"error":"Введите пароль и имя пользователья!"},status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username,password=password)
        if not user:
            return Response({"error":"Такого пользователья не сущестует!"})
        token , _ = Token.objects.get_or_create(user=user)
        user_function = UserFunctions(user=user)
        return Response(data={
            "from":"Login view",
            "data":user_function.detail(token_key=token.key)
        }
    )

class UserProfile(APIView):
    def get(self,request:Request):
        return Response({
            "from":"User Profile",
            "data":UserFunctions(user=request.user).detail(token_key=None)
            }
        )
        