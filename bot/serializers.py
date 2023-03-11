from rest_framework import serializers


class MessageSerializer(serializers.Serializer):
    message = serializers.CharField()
    sender_id = serializers.CharField()
