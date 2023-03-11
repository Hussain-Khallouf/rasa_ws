from rest_framework import routers
from .views import FAQViewSet

router = routers.SimpleRouter()
router.register(r'faqs', FAQViewSet)

urlpatterns = router.urls
