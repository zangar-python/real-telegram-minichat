from rest_framework.request import Request
from ..models import Chat
from django.contrib.auth.models import User
from accounts.user_serializer import UserSerializer
from ..serializer import ChatSerializer
from rest_framework.response import Response
# from django.shortcuts import get_object_or_404

class Chat_usersClass:
    def __init__(self,user:User,chat:Chat):
        self.chat : Chat = chat
        self.user : User = user
        pass
    
    def del_user_from_chat(self,id_user:int):
        res = self.if_user_in_this_chat()
        if res:
            return res
        
        if self.chat.users.filter(id=id_user).exists():
            self.chat.users.remove(id_user)
            data = {
                "connect":True,
                "id-obj-to-delete":id_user,
                "deleted":True
            }
            return self.get_result(data)
        else:
            data = {
                "connect":False,
                "id-obj-to-delete":id_user,
                "deleted":False,
                "error":"Такого пользователья в этом чате не существует"
            }
            return self.get_result(data=data)
    def add_user_to_chat(self,id_user:int):
        res = self.if_user_in_this_chat()
        if res:
            return res
        if self.chat.users.filter(id=id_user).exists():
            data = {
                "connect":False,
                "id-user-to-add":id_user,
                "error":"Пользователь уже в этом чате"
            }
            return self.get_result(data)
        if not User.objects.filter(id=id_user).exists():
            data = {
                "connect":False,
                "id-user-to-add":id_user,
                "error":"Пользователь с таким айди не существует"
            }
            return self.get_result(data)
        if self.chat.chat_type == "solo" and self.chat.users.all().count() >= 2:
            data = {
                "connect":False,
                "id-user-to-add":id_user,
                "error":"Этот чат для личной переписки а не групповой!"
            }
            return self.get_result(data=data)
        self.chat.users.add(id_user)
        data = {
            "id-user-to-add":id_user,
            "connect":True,
            "added":True
        }
        return self.get_result(data=data)
        
    def get_result(self,data):
        result = {
            "user":UserSerializer(self.user).data,
            "chat":ChatSerializer(self.chat).data,
            "connect":True,
            "data":data
        }
        return Response(data=result)
    def if_user_in_this_chat(self):
        if not self.chat.users.filter(id=self.user.id).exists(): 
            data = {
                "err":"Вы не состойте в этом чате!"
            }
            return self.get_result(data=data)
        return None