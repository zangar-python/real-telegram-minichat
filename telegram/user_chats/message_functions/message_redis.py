import redis
from redis_server_settings import REDIS_HOST,PORT,DB
from ..serializer import SoloMessageSerializer,SoloMessage

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
    def get_messages(chat_id):
        ids = [u.decode() for u in r.smembers(f"chat:{chat_id}:message_id")]
        
        messages = []
        for id in ids:
            message = r.hgetall(f"chat:{chat_id}:messages:{id}")
            messages.append({k.decode():v.decode() for k,v in message.items()})
        return messages
            
    