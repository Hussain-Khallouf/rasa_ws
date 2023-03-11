from drf_yasg.utils import swagger_auto_schema
from rasa.core.channels import UserMessage
from rest_framework.response import Response
from rest_framework.views import APIView

from core.bot_model import bot_model
from .serializers import MessageSerializer, TrainSerializer


# Create your views here.


class ChatAPIView(APIView):
    @swagger_auto_schema(request_body=MessageSerializer)
    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.data["message"]
        sender_id = serializer.data["sender_id"]
        message = UserMessage(text=message, sender_id=sender_id)
        response = bot_model.get_response(message)
        return Response(response)


class BotAPIView(APIView):
    @swagger_auto_schema(request_body=TrainSerializer)
    def put(self, request):
        bot_model.train()
        return Response("done")
