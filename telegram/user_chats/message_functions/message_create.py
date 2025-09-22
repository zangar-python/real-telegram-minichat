from ..models import SoloMessage,Chat
# from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .message_redis import MessageRedis
from ..serializer import ChatSerializer
from accounts.user_serializer import UserSerializer
from rest_framework.response import Response
from ..serializer import SoloMessageSerializer

class Message_classCreate:
    def __init__(self,chat,text,user:User):
        self.chat = chat
        self.text = text
        self.user = user
        pass
    def get_result(self,data):
        obj = {
            "user":UserSerializer(self.user).data,
            "chat":ChatSerializer(self.chat).data,
            "connect":True,
            "data":data
        }
        return Response(data=obj)
    def create(self):
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