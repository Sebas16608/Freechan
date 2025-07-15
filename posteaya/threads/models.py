from django.db import models
from boards.models import Board
import random
import string
# Create your models here.

# genera un id random y anonimo
def generar_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

# Threads
class Thread(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='Board')
    titulo = models.CharField(max_length=255, blank=True)
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='media/')
    creado = models.DateTimeField(auto_now_add=True)
    conectado = models.DateTimeField(auto_now_add=True)
    id_an = models.CharField(max_length=8, editable=False, unique=False)

    def save(self, *args, **kwargs):
        if not self.id_an:
            self.id_an = generar_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = "Thread"
        verbose_name_plural = "Threads"
    