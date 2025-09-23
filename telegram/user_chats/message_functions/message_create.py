from ..models import SoloMessage,Chat
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .message_redis import MessageRedis
from ..serializer import ChatSerializer
from accounts.user_serializer import UserSerializer
from rest_framework.response import Response
from ..serializer import SoloMessageSerializer

class Message_classCreate:
    def __init__(self,chat,text,user:User):
        self.chat :Chat = chat
        self.text = text
        self.user:User = user
        pass
    def get_result(self,data):
        obj = {
            "user":UserSerializer(self.user).data,
            "chat":ChatSerializer(self.chat).data,
            "connect":True,
            "data":data
        }
        return Response(data=obj)
    @staticmethod
    def is_user_in_this_chat(user_id,chat_id):
        chat = get_object_or_404(Chat,id=chat_id)
        if chat.users.filter(id=user_id).exists():
            return None
        data = {
            "err":"Вы не являетесь участником этого чата",
            "Error":True,
            "user":user_id,
            "chat":ChatSerializer(chat).data
        }
        return Response(data)
    def create(self):
        user_in_this_chat = self.is_user_in_this_chat(user_id=self.user.id,chat_id=self.chat.id)
        if user_in_this_chat:
            return user_in_this_chat
        message = SoloMessage.objects.create(chat=self.chat,from_user=self.user,text=self.text)
        res = MessageRedis.add_message(self.chat.id,message.id,message)
        if res:
            message.delete()
            return self.get_result(res)
        data = {
            "created":True,
            "model":SoloMessageSerializer(message).data
        }
        return self.get_result(data)