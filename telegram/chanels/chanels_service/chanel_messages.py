from django.shortcuts import get_object_or_404
from ..models import Message,Chanel
from .chanals_redis import ChanalRedis
from rest_framework.response import Response
from ..serializer import MessageSerializer

class MessageChanels:
    def __init__(self,request):
        self.user = request.user
        pass
    def result(self,data):
        res = {
            "user":self.user.username,
            "user_id":self.user.id,
            "chanel_id":self.chanel.id,
            "data":data
        }
        return Response(res)
    def set_chanel(self,chanel_id):
        self.chanel = get_object_or_404(Chanel,id=chanel_id)
        return
    def is_user_in_this_chat(self):
        if self.chanel.users.filter(id=self.user.id).exists():
            return True
        return False
    def is_user_admin(self):
        if self.chanel.admins.filter(id=self.user.id).exists():
            return True
        return False
    def create_message(self,text):
        res = self.is_user_admin()
        if not res:
            return self.result("user is not admin")
        message = Message.objects.create(
            text=text,chanel=self.chanel,user=self.user
        )
        ChanalRedis.set_message(message)
        return self.result({
            "created":True,
            "message":MessageSerializer(message).data
        })
    def get_chanel_messages(self):
        if self.chanel.private :
            is_user = self.is_user_in_this_chat()
            is_admin = self.is_user_admin()
            if not is_user and not is_admin:
                return self.result("Вы не являетесь пользователем этого закрытого канала")
        msgs = ChanalRedis.get_chanel_messages(self.chanel)
        return self.result(msgs)