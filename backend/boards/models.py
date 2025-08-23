from django.db import models

# Create your models here.
class Board(models.Model):
    titulo = models.CharField(max_length=255)
    short_name = models.CharField(max_length=100, blank=False, default="BN")
    descripcion = models.TextField()
    portada = models.ImageField(upload_to="")
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Board"
        verbose_name_plural = "Boards"

    def __str__(self):
        return self.titulo
    
class Lista(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='board')