from .chat_functions.chat_detail import CreateChat
from .chat_functions.chat_users import Chat_usersClass
from .chat_functions.chat_redis import RedisChat
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from accounts.user_class import UserFunctions
from django.shortcuts import get_object_or_404
from .models import Chat

from .message_functions.message_create import Message_classCreate
from .message_functions.message_redis import MessageRedis

class ChatsViews(APIView):
    def post(self,request:Request):
        chat_class = CreateChat(request=request)
        if chat_class.user_is_created() == False:
            data = {
                "Неправильно введен айди пользователей"
            }
            return chat_class.result_chat(data)
        return chat_class.create_chat_res()
    def get(self,request:Request):
        data = UserFunctions(user=request.user).result(data=CreateChat.get_users_chats(request))
        return Response(data=data)
class ChatsDetailView(APIView):
    def get(self,request:Request,id):
        data = UserFunctions(user=request.user).result(RedisChat.get_chat_by_id(id=id))
        return Response(data=data)
    def delete(self,request:Request,id):
        data = UserFunctions(user=request.user).result(CreateChat.delete_chat_by_id(id))
        return Response(data=data)

class chat_users_add_delete(APIView):
    def post(self,request:Request,id):
        chat = get_object_or_404(Chat,id=id)
        users_id = request.data.get("users")
        if not users_id:
            data = "Введите айди пользователей"
            res = UserFunctions(user=request.user).result(data=data)
            return Response(data=res)
        return Chat_usersClass(request.user,chat).add_many_users_to_chat(users_id)
    def delete(self,request:Request,id):
        chat = get_object_or_404(Chat,id=id)
        users_id = request.data.get("users")
        print("Правильно")
        if not users_id:
            print("Воот ЗДЕСЬ")
            data = "Введите айди пользователей"
            res = UserFunctions(user=request.user).result(data=data)
            return Response(data=res)
        return  Chat_usersClass(request.user,chat).delete_many_users(users_id)
class MessagesViews(APIView):
    def post(self,request:Request,id):
        chat = get_object_or_404(Chat,id=id)
        text = request.data.get("text")
        if not text:
            return Response(UserFunctions(request.user).result("Введите текст"))
        message = Message_classCreate(chat=chat,text=text,user=request.user)
        return message.create()
    def get(self,request:Request,id):
        if not Chat.objects.filter(id=id).exists():
            return Response(UserFunctions(request.user).result("Неправильные данные по айди"))
        return Response(data=UserFunctions(request.user).result(MessageRedis.get_messages(chat_id=id,user_id=request.user.id)))