from rest_framework.request import Request
from rest_framework.response import Response
from django.contrib.auth.models import User
from .chanals_redis import ChanalRedis
from ..models import Chanel
from ..serializer import ChanelSerializer
from django.shortcuts import get_object_or_404

class ChanelsClass:
    def __init__(self,request:Request):
        self.user : User = request.user
        
    def result(self,data):
        result = {
            "user":self.user.username,
            "id":self.user.id,
            "email":self.user.email,
            "data":{
                "connected":True,
                "detail":data
            }
        }
        return Response(data=result)
    
    def get_datas_from_request(self,request:Request):
        name = request.data.get("name")
        more = request.data.get("more","")
        private = request.data.get("private",False)
        if not name:
            return {
                "err":True,
                "text":"Вы не показали имя канала"
            }
        if Chanel.objects.filter(name=name).exists():
            return {
                "err":True,
                "text":"Канал с таким же названием существует"
            }
        self.name = name
        self.more = more
        self.private = private
        return
    
    def user_is_admin(self,chanel_id):
        chanel = get_object_or_404(Chanel,id=chanel_id)
        if chanel.admins.filter(id=self.user.id).exists():
            return True
        return False
        
    def add_users_to_chanal(self,chanel_id,request:Request):
        if not self.user_is_admin(chanel_id):
            return self.result("you'r not a admin")
        users = request.data.get("users",[])
        chanel = get_object_or_404(Chanel,id=chanel_id)
        chanel.users.add(*users)
        ChanalRedis.add_users([u_id.id for u_id in chanel.users.all()],chanel_id)
        return self.result("added!")
    def user_register_to_chanal(self,chanel_id):
        chanel = get_object_or_404(Chanel,id=chanel_id)
        if chanel.users.filter(id=self.user.id).exists() or chanel.admins.filter(id=self.user.id).exists():
            return self.result("Вы уже участник этого канала")
        if chanel.private:
            return self.result("Этот канал приватный")
        chanel.users.add(self.user)
        ChanalRedis.add_users([self.user.id],chanel_id)
        return self.result("Вы зашли в канал")
        
    def create_chanel(self):
        
        chanel = Chanel.objects.create(
            name=self.name,
            more=self.more,
            private=self.private
        )
        chanel.admins.add(self.user)
        ChanalRedis.createChanel(self.user.id,chanel.id,chanel.name,chanel.more,chanel.private)
        return self.result(data=ChanelSerializer(chanel).data)
    
    def get_user_chanels(self):
        chanel_ids = [ch.id for ch in self.user.chanels.all()]
        user_chanel_ids = [ch.id for ch in self.user.my_chanels.all()]
        data = ChanalRedis.get_chanel([*chanel_ids,*user_chanel_ids])
        return self.result(data)
