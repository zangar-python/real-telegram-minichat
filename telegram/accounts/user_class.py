from django.contrib.auth.models import User
from .user_serializer import UserSerializer

import redis
r = redis.Redis(host="localhost",port=6379,db=0)

class UserFunctions():
    def __init__(self,user:User):
        self.user = user
        pass
    def user_register_to_redis(self):
        try:
            user = {
                "username":self.user.username,
                "id":self.user.id,
                "password":self.user.password
            }
            r.hset(f"user:{self.user.id}",mapping=user)
            print("user is registered")
            return True
        except Exception as e:
            print("error",e)
            return False
    def detail(self,token_key):
        data = {
            "user":UserSerializer(self.user).data,
            "token":token_key,
            "connected":True
        }
        return data
    
    def result(self,data):
        obj = {
            "request":True,
            "from_user":self.user.username,
            "id_user":self.user.id,
            "email_user":self.user.email,
            "data":data,
            "connect":"Is Connected"
        }
        return obj
    
    def GetAllUsers(self):
        users = User.objects.all()
        return self.result(UserSerializer(users,many=True).data)
    