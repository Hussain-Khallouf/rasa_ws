from django.db import models


class Intent(models.Model):
    name = models.CharField(max_length=255)


class IntentExample(models.Model):
    text = models.CharField(max_length=1024)
    intent = models.ForeignKey(Intent, on_delete=models.CASCADE, related_name="examples", null=True)
