from django.db import models
from threads.models import Thread
# Create your models here.
from django.db import models
from threads.models import Thread
# Create your models here.

class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="posts")
    contenido = models.TextField()
    imagen = models.ImageField(upload_to="media", null=True, blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"