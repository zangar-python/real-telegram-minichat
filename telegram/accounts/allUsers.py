from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from .user_class import UserFunctions
from django.contrib.auth.models import User

class GetAllUsersViews(APIView):
    def get(self,request:Request):
        user = request.user
        data = UserFunctions(user=user).get_all_users_from_redis()
        return Response(
            data=data
        )

class DeleteUser(APIView):
    def delete(self,request:Request):
        
        if not User.objects.filter(id=request.user.id).exists:
            return Response({"error":"Аномалия"})
        user = User.objects.get(id=request.user.id)
        user.delete()
        return Response("User is deleted")