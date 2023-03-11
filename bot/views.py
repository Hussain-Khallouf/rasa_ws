from drf_yasg.utils import swagger_auto_schema
from rasa.core.channels import UserMessage
from rest_framework.response import Response
from rest_framework.views import APIView
from core.bot_model import bot_model
from .serializers import MessageSerializer


# Create your views here.


class ChatAPIView(APIView):
    @swagger_auto_schema(request_body=MessageSerializer)
    def post(self, request):
        message = request.data["message"]
        message = UserMessage(text=message)
        response = bot_model.get_response(message)
        return Response(response)
