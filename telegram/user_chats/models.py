from django.db import models

from django.contrib.auth.models import User

# Create your models here.

CHAT_TYPE_CHOICES = [
    ("solo","Личный"),
    ("many","Групповой")
]

class Chat(models.Model):
    users = models.ManyToManyField(User,related_name="chats")
    chat_name = models.CharField(max_length=50)
    chat_type = models.CharField(choices=CHAT_TYPE_CHOICES,max_length=10,default="solo")
    
    def __str__(self):
        return self.chat_name

class SoloMessage(models.Model):
    text = models.TextField(null=False)
    from_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="my_messages")
    sended_at = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey(Chat,on_delete=models.CASCADE,related_name="messages")
    
    class Meta:
        ordering = ["sended_at"]
    
    def __str__(self):
        return f"{self.from_user} : {self.text[:10]}..."