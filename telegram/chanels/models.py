from django.db import models
from django.contrib.auth.models import User




# Create your models here.
class Chanel(models.Model):
    name = models.CharField(max_length=120)
    more = models.CharField(max_length=400,null=True)
    admins = models.ManyToManyField(User,related_name="my_chanels")
    users = models.ManyToManyField(User,related_name="chanels")
    private = models.BooleanField(default="false")

class Message(models.Model):
    chanel = models.ForeignKey(Chanel,on_delete=models.CASCADE,related_name="messages")
    text = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="messages")
    created_at = models.DateTimeField(auto_now_add=True)