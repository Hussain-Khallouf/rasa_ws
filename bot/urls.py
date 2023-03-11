from django.urls import path

from .views import ChatAPIView

urlpatterns = [
    path("test/", ChatAPIView.as_view())
]
