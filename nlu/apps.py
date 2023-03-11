from django.apps import AppConfig


class NluConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "nlu"
    def ready(self):
        from . import signals