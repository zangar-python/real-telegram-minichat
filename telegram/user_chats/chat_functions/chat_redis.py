import redis
from redis_server_settings import REDIS_HOST,PORT,DB

r = redis.Redis(host=REDIS_HOST,port=PORT,db=DB)

class RedisChat:
    def __init__(self,chat_name:str,chat_type:str,users:list[int],chat_id:str):
        self.chat = {
            "name":chat_name,
            "type":chat_type,
            "id":chat_id
        }
        self.name = f"chat:{chat_id}"
        self.id = chat_id
        self.users = users
        pass
    def create_chat(self):
        try:
            r.sadd("chat_id",self.id)
            r.hset(self.name,mapping=self.chat)
            r.sadd(f"{self.name}:users",*self.users)
            print("REDIS chat is created")
            return True
        except Exception as e:
            print(e)
            return False
    @staticmethod
    def get_chat_by_id(id):
        chat = r.hgetall(f"chat:{id}")
        if not chat:
            return None
        users = r.smembers(f"chat:{id}:users")
        
        chat = {k.decode():v.decode() for k,v in chat.items()}
        users = [int(u.decode()) for u in users]
        
        chat["users"] = users
        return chat
    @staticmethod 
    def get_all_chats(chats_id):
        chats = []
        for id in chats_id:
            chat = RedisChat.get_chat_by_id(id=id)
            if chat:
                chats.append(chat)
            else:
                r.srem("chat_id",id)
        print(chats)
        return chats
    @staticmethod 
    def delete_chat_by_id(id):
        try:
            r.delete(f"chat:{id}")
            r.delete(f"chat:{id}:users")
            r.srem("chat_id",id)
            return True
        except Exception as e:
            print("REDIS ERROR DELETE",e)
            return False
    @staticmethod
    def delete_user_from_chat(user_id,chat_id):
        if not r.sismember(f"chat:{chat_id}:users",user_id):
            return {
                "err":True,
                "text":"Пользователь не существует"
            }
        r.srem(f"chat:{chat_id}:users",user_id)
        return None      
    @staticmethod
    def add_user_to_chat(user_id,chat_id):
        try:
            r.sadd(f"chat:{chat_id}:users",user_id)
            return None
        except Exception as e:
            print(e)
            return {
                "err":True,
                "text":"Что-то пошло не так"
            }
    @staticmethod
    def add_users_to_chatMany(users_id,chat_id):
        try:
            r.sadd(f"chat:{chat_id}:users",*users_id)
            return None
        except Exception as e:
            print(e)
            return {
                "err":True,
                "text":"Что-то пошло не так"
            }
    @staticmethod 
    def delete_many_users_from_chat(users_id,chat_id):
        try:
            r.srem(f"chat:{chat_id}:users",*users_id)
            return None
        except Exception as e:
            print(e)
            return {
                "err":True,
                "text":"Что-то пошло не так"
            }