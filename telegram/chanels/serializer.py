from rest_framework.serializers import ModelSerializer
from .models import Chanel,Message

class ChanelSerializer(ModelSerializer):
    class Meta:
        model = Chanel
        fields = "__all__"
class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
