from rest_framework.request import Request
from ..models import Chat
from django.contrib.auth.models import User
from accounts.user_serializer import UserSerializer
from ..serializer import ChatSerializer
from rest_framework.response import Response
class CreateChat:
    def __init__(self,request:Request):
        self.user : User = request.user
        self.chat_type = self.chat_type_method(request)
        self.users = self.get_users(request)
        self.chat_name = self.chat_name_setting(request)
        pass
    def chat_type_method(self,request:Request):
        type = request.data.get("type")
        if not type:
            return "solo"
        return type
    def get_users(self,request:Request):
        users : list[int] = request.data.get("users",[])
        if self.user.id not in users :
            users.append(self.user.id)
        return users
    def chat_name_setting(self,request:Request):
        if self.chat_type != "many":
            if len(self.users) >= 2:
                username1 = User.objects.get(pk=self.users[0]).username
                username2 = User.objects.get(pk=self.users[1]).username
                return f"{username1} and {username2}"
            else:
                return f"{username1} chat"
        chat_name = request.data.get("chat_name")
        if not chat_name:
            return "Групповой чат"
        return chat_name
    
    
    def create_chat_res(self):
        chat = Chat.objects.create(
            chat_type=self.chat_type,
            chat_name=self.chat_name,
        )
        users = User.objects.filter(id__in=self.users)
        chat.users.add(*users)
        chat.save()
        return self.result_chat(ChatSerializer(chat).data)
    def is_chat_solo(self):
        if len(self.users) > 2 and self.chat_type == "solo":
            return Response(data={
                "err":"solo chat but users > 2",
                "users":self.users,
                "type":self.chat_type
            })
        return  None
        
    def result_chat(self,res_data):
        err = self.is_chat_solo()
        if err:
            return err 
        res = {
            "user":UserSerializer(self.user).data(),
            "connect":True,
            "self_data":{
                "chat_type":self.chat_type,
                "chat_name":self.chat_name,
                "users":self.users
            },
            "result-data":res_data
        }
        return Response(data=res)