from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.contrib.auth.models import User
import redis
from redis_server_settings import PORT,REDIS_HOST,DB

r = redis.Redis(host=REDIS_HOST,port=PORT,db=DB)

@receiver(post_delete,sender=User)
def DeleteUserFromRedis(sender,instance:User,**kwargs):
    r.hdel(f"user:{instance.id}")