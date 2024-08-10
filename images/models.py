# models.py
from django.db import models
import uuid

class GeneratedImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task_id = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    prompt = models.TextField()
