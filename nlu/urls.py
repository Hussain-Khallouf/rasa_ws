from rest_framework import routers
from .views import IntentViewSet

router = routers.SimpleRouter()
router.register(r'intents', IntentViewSet)

urlpatterns = router.urls
