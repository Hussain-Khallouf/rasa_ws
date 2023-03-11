from django.db import models


# Create your models here.

class FAQ(models.Model):
    question = models.TextField(max_length=1024)
    text_response = models.TextField(max_length=1024)
    image_response = models.TextField(max_length=1024, null=True)
