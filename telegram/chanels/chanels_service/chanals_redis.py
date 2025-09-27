import redis
from redis_server_settings import REDIS_HOST,PORT,DB
from rest_framework.request import Request
from django.contrib.auth.models import User
from ..serializer import MessageSerializer,Message

r = redis.Redis(host=REDIS_HOST,port=PORT,db=DB)

class ChanalRedis:
    # def __init__(self,request:Request):
    #     self.user:User = request.user
    #     pass
    @staticmethod
    def get_chanel(ids):
        res = []
        for id in ids:
            chanel = ChanalRedis.decoding_dict(r.hgetall(f"chanel:{id}"))
            chanel["id"] = id
            res.append(chanel)
        return res
    
    @staticmethod
    def set_message(msg):
        r.hset(f"chanel:{msg.chanel.id}:message:{msg.id}",mapping=MessageSerializer(msg).data)
        r.sadd(f"chanel:{msg.chanel.id}:messages_id",msg.id)
        return
    @staticmethod
    def get_chanel_messages(chanel):
        ids = [i.decode() for i in r.smembers(f"chanel:{chanel.id}:messages_id")]
        msgs = []
        for id in ids:
            message = r.hgetall(f"chanel:{chanel.id}:message:{id}")
            decoded_msg = ChanalRedis.decoding_dict(message)
            msgs.append(decoded_msg)
        return msgs
        
    
    @staticmethod
    def decoding_dict(obj):
        return {k.decode():v.decode() for k,v in obj.items()} 
    
    @staticmethod
    def add_users(users,chanel_id): 
        r.sadd(f"chanel:{chanel_id}:users",*users)
        return
    @staticmethod
    def createChanel(admin_id,id,name,more,private):
        r.hset(f"chanel:{id}",mapping={
            "name":name,
            "more":str(more),
            "private":str(private)
        })
        r.sadd("chanels_id",id)
        r.sadd(f"chanel:{id}:admins",admin_id)
        return
    @staticmethod 
    def add_admins(admins,chanel_id):
        r.sadd(f"chanel:{chanel_id}:admins",*admins)