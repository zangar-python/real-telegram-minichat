from rest_framework.request import Request
from ..models import Chat
from django.contrib.auth.models import User
from accounts.user_serializer import UserSerializer
from ..serializer import ChatSerializer
from rest_framework.response import Response
# from django.shortcuts import get_object_or_404
from .chat_redis import RedisChat

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
            
            redis_request_err = RedisChat.delete_user_from_chat(id_user,self.chat.id)
            if redis_request_err:
                return self.get_result(redis_request_err)
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
        redis_err = RedisChat.add_user_to_chat(id_user,self.chat.id)
        if redis_err:
            self.chat.users.remove(id_user)
            return self.get_result(data=redis_err)
        data = {
            "id-user-to-add":id_user,
            "connect":True,
            "added":True
        }
        return self.get_result(data=data)
    def add_many_users_to_chat(self,users_id):
        res = self.if_user_in_this_chat()
        if res:
            return res
        if not self.users_is_created(users_id):
            data = {
                "Error":True,
                "text_":"Вы добавили не существующий айди пользователья"
            }
            return self.get_result(data=data)
        if not self.if_users_in_this_chat(users_id):
            data = {
                "Error":True,
                "text_":"Некоторые пользователи уже в этом чате"
            }
            return self.get_result(data=data)
        if self.chat.users.count() + len(users_id) > 2 and self.chat.chat_type == "solo":
            data = {
                "Error":True,
                "text_":"Этот чат для двух пользователей."
            }
            return self.get_result(data=data)
        self.chat.users.add(*users_id)
        err_redis = RedisChat.add_users_to_chatMany(users_id,self.chat.id)
        if err_redis:
            self.chat.users.remove(*users_id)
            return self.get_result(err_redis)
        data = {
            "users_added":True,
            "users":users_id,
        }
        return self.get_result(data=data)
                
    @staticmethod
    def users_is_created(users_id):
        for id in users_id:
            if not User.objects.filter(id=id).exists():
                return False
        return True
    
    def if_users_in_this_chat(self,users_id):
        if self.chat.users.filter(id__in=users_id).exists():
            return False
        return True
        
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
    
    def delete_many_users(self,users_id):
        res = self.if_user_in_this_chat()
        if res:
            return res
        self.chat.users.remove(*users_id)
        err_redis = RedisChat.delete_many_users_from_chat(users_id,self.chat.id)
        if err_redis:
            self.chat.users.add(*users_id)
            return self.get_result(err_redis)
        return self.get_result("Удалено из чата")
    