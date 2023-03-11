from rest_framework import viewsets

from core.utils import CstmModelViewSet
from .models import Intent
from .serializers import IntentSerializer


class IntentViewSet(CstmModelViewSet):
    queryset = Intent.objects.prefetch_related("examples").all()
    serializer_class = IntentSerializer
