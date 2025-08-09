from django.db import models
from threads.models import Thread
# Create your models here.

class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="posts")
    contenido = models.TextField()
    creado = models.DateTimeField(auto_now_add=True)