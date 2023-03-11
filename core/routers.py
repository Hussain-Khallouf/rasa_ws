from django.urls import path, include

urlpatterns = [
    path("", include("faq.urls")),
    path("", include("nlu.urls")),
]
