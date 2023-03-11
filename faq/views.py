from core.utils import CstmModelViewSet
from .models import FAQ
from .serializers import FAQSerializer


class FAQViewSet(CstmModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
