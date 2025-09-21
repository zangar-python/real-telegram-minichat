from .chat_functions.chat_detail import CreateChat
from .chat_functions.chat_users import Chat_usersClass
from .chat_functions.chat_redis import RedisChat
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from accounts.user_class import UserFunctions

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
        data = UserFunctions(user=request.user).result(data=RedisChat.get_all_chats())
        return Response(data=data)
class ChatsDetailView(APIView):
    def get(self,request:Request,id):
        data = UserFunctions(user=request.user).result(RedisChat.get_chat_by_id(id=id))
        return Response(data=data)
    def delete(self,request:Request,id):
        data = UserFunctions(user=request.user).result(CreateChat.delete_chat_by_id(id))
        return Response(data=data)