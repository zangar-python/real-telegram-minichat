import redis
from redis_server_settings import REDIS_HOST,PORT,DB
from ..serializer import SoloMessageSerializer,SoloMessage
from django.shortcuts import get_object_or_404
from ..models import Chat

r = redis.Redis(host=REDIS_HOST,port=PORT,db=DB)

class MessageRedis:
    @staticmethod
    def add_message(chat_id,msg_id,msg:SoloMessage):
        try:
            message = SoloMessageSerializer(msg).data
            r.hset(f"chat:{chat_id}:messages:{msg_id}",mapping=message)
            r.sadd(f"chat:{chat_id}:message_id",msg_id)
            return None
        except Exception as e:
            print(e)
            return {"Err":True,"data":"Что-то пошло не так"}
    @staticmethod
    def in_this_chat(user_id,chat_id):
        chat = get_object_or_404(Chat,id=chat_id)
        if chat.users.filter(id=user_id).exists():
            return None
        return "Вы не являетесь пользователем этого чата"
    
    @staticmethod 
    def get_messages(chat_id,user_id):
        in_this_chat = MessageRedis.in_this_chat(user_id=user_id,chat_id=chat_id)
        if in_this_chat:
            return in_this_chat
        ids = [u.decode() for u in r.smembers(f"chat:{chat_id}:message_id")]        
        messages = []
        for id in ids:
            message = r.hgetall(f"chat:{chat_id}:messages:{id}")
            messages.append({k.decode():v.decode() for k,v in message.items()})
        return messages
            
    