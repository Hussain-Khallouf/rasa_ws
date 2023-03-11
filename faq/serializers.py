from rest_framework import serializers

from .models import FAQ


class FAQSerializer(serializers.ModelSerializer):
    image_response = serializers.CharField(allow_null=True, required=False)

    class Meta:
        model = FAQ
        fields = (
            "id",
            "question",
            "text_response",
            "image_response"
        )
