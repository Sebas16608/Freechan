from django.db import models
from threads.models import Thread
from django.utils import timezone
# Create your models here.

class Posts(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='Thread')
    post = models.TextField()
    image = models.ImageField(upload_to="media", blank=True)
    creado = models.DateTimeField(default=timezone.now)
    respuesta = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replis')

    def __str__(self):
        return f"Post en {self.thread}"

    