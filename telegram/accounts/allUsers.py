from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from .user_class import UserFunctions

class GetAllUsersViews(APIView):
    def get(self,request:Request):
        user = request.user
        data = UserFunctions(user=user).GetAllUsers()
        return Response(
            data=data
        )