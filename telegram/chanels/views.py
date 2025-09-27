from rest_framework.views import APIView
from .chanels_service.chanels_class import ChanelsClass
from rest_framework.response import Response
from rest_framework.request import Request
from accounts.user_class import UserFunctions
from .chanels_service.chanel_messages import MessageChanels

class ChanelViews(APIView):
    def get(self,request:Request):
        return ChanelsClass(request).get_user_chanels()
    def post(self,request:Request):
        chanal_with_user = ChanelsClass(request)
        is_err = chanal_with_user.get_datas_from_request(request)
        if is_err:
            return Response(UserFunctions(request.user).result(is_err))
        return chanal_with_user.create_chanel()

class chanel_detail_view(APIView):
    def post(self,request:Request,id):
        msg_class = MessageChanels(request)
        msg_class.set_chanel(id)
        text = request.data.get("text")
        if not text:
            return Response({"err":True,"text":"Введите текст.Вы хотите отправить пустой текст?"})
        return msg_class.create_message(text)
    def get(self,request:Request,id):
        msg_class = MessageChanels(request)
        msg_class.set_chanel(id)
        return msg_class.get_chanel_messages()
class register_to_chanel_views(APIView):
    def post(self,request:Request,id):
        chanel_class = ChanelsClass(request)
        return chanel_class.user_register_to_chanal(id)
    def delete(self,request:Request,id):
        chanel_class = ChanelsClass(request)
        return chanel_class.user_unregistered(id)

class user_channel_views(APIView):
    def post(self,request:Request,id):
        chanel_class = ChanelsClass(request)
        return chanel_class.add_users_to_chanal(id,request)
    def delete(self,request:Request,id):
        channel_class = ChanelsClass(request)
        users_id = request.data.get("users",[])
        return channel_class.delete_user_from_chanel(users_id,id)
    def get(self,request:Request,id):
        channel_class = ChanelsClass(request)
        return channel_class.get_users_channel(id)
        