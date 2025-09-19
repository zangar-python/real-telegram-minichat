from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.contrib.auth.models import User
import redis

r = redis.Redis(host="localhost",port=6379,db=0)

@receiver(post_delete,sender=User)
def DeleteUserFromRedis(sender,instance:User,**kwargs):
    r.hdel(f"user:{instance.id}")