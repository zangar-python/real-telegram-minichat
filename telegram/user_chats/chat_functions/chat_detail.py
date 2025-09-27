from rest_framework.request import Request
from ..models import Chat
from django.contrib.auth.models import User
from accounts.user_serializer import UserSerializer
from ..serializer import ChatSerializer
from rest_framework.response import Response
from .chat_redis import RedisChat
from django.shortcuts import get_object_or_404

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
        elif type != "solo" and type != "many":
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
        err = self.is_chat_solo()
        if err:
            return err 
        chat = Chat.objects.create(
            chat_type=self.chat_type,
            chat_name=self.chat_name,
        )
        users = User.objects.filter(id__in=self.users)
        chat.users.add(*users)
        chat.save()
        if not self.create_in_redis(chat.id):
            chat.delete()
            return self.result_chat("чат не создан в редис")
        return self.result_chat(ChatSerializer(chat).data)
    def create_in_redis(self,chat_id):
        redis_chat = RedisChat(self.chat_name,self.chat_type,self.users,chat_id)
        return redis_chat.create_chat()
    
    def is_chat_solo(self):
        if len(self.users) > 2 and self.chat_type == "solo":
            return Response(data={
                "err":"solo chat but users > 2",
                "users":self.users,
                "type":self.chat_type
            })
        return  None
    def user_is_created(self):
        for user_id in self.users:
            if not User.objects.filter(id=user_id).exists():
                return False
        return True
    
    def result_chat(self,res_data):
        res = {
            "user":UserSerializer(self.user).data,
            "connect":True,
            "self_data":{
                "chat_type":self.chat_type,
                "chat_name":self.chat_name,
                "users":self.users
            },
            "result-data":res_data
        }
        return Response(data=res)
    
    @staticmethod 
    def delete_chat_by_id(id):
        chat = get_object_or_404(Chat,id=id)
        chat.delete()
        if RedisChat.delete_chat_by_id(id) == False:
            return "Не удален в Redis"
        return "Удален успешно"
    
    @staticmethod 
    def get_users_chats(request:Request):
        user : User = request.user
        chats_id = [chat.id for chat in user.chats.all()]
        return RedisChat.get_all_chats(chats_id)
    
    @staticmethod
    def get_all_chats():
        chats = Chat.objects.all()
        return ChatSerializer(chats,many=True).data