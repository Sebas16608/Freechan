from django.db import models

# Create your models here.
class Board(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    portada = models.ImageField(upload_to="media")
    create_at = models.DateTimeField(auto_now_add=True)