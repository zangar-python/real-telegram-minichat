from django.contrib.auth.models import User
from .user_serializer import UserSerializer

import redis
from redis_server_settings import PORT,REDIS_HOST,DB

r = redis.Redis(host=REDIS_HOST,port=PORT,db=DB)

class UserFunctions():
    def __init__(self,user:User):
        self.user = user
        pass
    def user_register_to_redis(self):
        try:
            user = {
                "username":self.user.username,
                "id":self.user.id,
            }
            r.hset(f"user:{self.user.id}",mapping=user)
            r.sadd("users",self.user.id)
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
    def decode_dict(self,data:dict):
        return {k.decode():v.decode() for k,v in data.items()}
    
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
    
    def get_all_users_from_redis(self):
        users = []
        for user_id in r.smembers("users"):
            user = r.hgetall(f"user:{user_id.decode()}")
            users.append(self.decode_dict(user))
        print(users)
        return self.result(users)