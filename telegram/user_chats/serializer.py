from rest_framework.serializers import ModelSerializer
from .models import Chat,SoloMessage

class ChatSerializer(ModelSerializer):
    class Meta:
        model = Chat
        fields = "__all__"

class SoloMessageSerializer(ModelSerializer):
    class Meta:
        model = SoloMessage
        fields = "__all__"