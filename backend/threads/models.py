from django.db import models
from boards.models import Board
# Create your models here.

class Thread(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='board')
    titulo = models.CharField(max_length=255)
    contenido = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    feautered = models.BooleanField(default=False)
    update = models.BooleanField(default=True)

    class Meta:
        verbose_name = "thread"
        verbose_name_plural = "threads"

    def __str__(self):
        return self.titulo