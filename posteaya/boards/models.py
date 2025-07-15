from django.db import models

# Create your models here.

#Boards
class Board(models.Model):
    name = models.CharField(max_length=255)
    short_name = models.SlugField(max_length=50)
    descripcion = models.TextField()
    visible = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Board"
        verbose_name_plural = "Boards"